
from threading import Lock
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from app.orchestration.graph import concern_graph


router = APIRouter()


class ChatRequest(BaseModel):
    """Information sent by the citizen to the chat API."""

    message: str = Field(min_length=1)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Information returned to the frontend after processing a message."""

    conversation_id: str
    reply: str
    department: str | None = None
    status: str
    extracted_details: dict[str, Any] = Field(default_factory=dict)
    missing_fields: list[str] = Field(default_factory=list)


# Temporary conversation storage.
# Data is lost when the backend process restarts.
conversation_store: dict[str, dict[str, Any]] = {}
conversation_lock = Lock()


def prepare_conversation_state(
    message: str,
    previous_state: dict[str, Any] | None,
) -> dict[str, Any]:
    """
    Prepare the conversation state for LangGraph.

    New conversations start with the citizen's first message.
    Existing conversations include previous messages and state.
    """
    new_message = HumanMessage(content=message)

    if previous_state is None:
        return {
            "messages": [new_message],
            "department": None,
            "status": "new",
        }

    return {
        **previous_state,
        "messages": [
            *previous_state["messages"],
            new_message,
        ],
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a citizen message through the concern workflow.

    Create or continue a conversation, run LangGraph,
    and return the agent's response to the frontend.
    """
    conversation_id = request.conversation_id or str(uuid4())

    with conversation_lock:
        previous_state = conversation_store.get(conversation_id)

        # An existing conversation ID must belong to a saved conversation.
        if request.conversation_id and previous_state is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found. Start a new conversation.",
            )

        state = prepare_conversation_state(
            message=request.message,
            previous_state=previous_state,
        )

        # Process the message using the Supervisor or department agent.
        result = concern_graph.invoke(state)

        # Keep the updated state for the next citizen message.
        conversation_store[conversation_id] = result

    return ChatResponse(
        conversation_id=conversation_id,
        reply=str(result["messages"][-1].content),
        department=result.get("department"),
        status=result.get("status", "needs_clarification"),
        extracted_details=result.get("extracted_details", {}),
        missing_fields=result.get("missing_fields", []),
    )
