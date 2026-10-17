
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.registry import get_available_agents
from app.agents.supervisor.prompts import SUPERVISOR_SYSTEM_PROMPT
from app.core.llm import get_llm
from app.orchestration.state import ConcernState


def supervisor_agent(state: ConcernState) -> dict:
    """
    Identify which department should handle a citizen's concern.

    The Supervisor reads the latest citizen message,
    selects a department using the LLM, and validates
    the selection against the agent registry.
    """

    available_agents = get_available_agents()

    # Prepare department descriptions for the LLM.
    department_descriptions = "\n".join(
        f"- {department}: {details['description']}"
        for department, details in available_agents.items()
    )

    system_prompt = SUPERVISOR_SYSTEM_PROMPT.format(
        available_departments=department_descriptions
    )

    # Find the latest message sent by the citizen.
    messages = state.get("messages", [])

    latest_user_message = next(
        (
            message.content
            for message in reversed(messages)
            if isinstance(message, HumanMessage)
        ),
        None,
    )

    if latest_user_message is None:
        return {
            "department": None,
            "status": "needs_clarification",
        }

    # Ask the LLM to identify the appropriate department.
    llm = get_llm()

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=str(latest_user_message)),
    ])

    selected_department = str(response.content).strip().lower()

    # Reject departments that are not registered.
    if selected_department not in available_agents:
        return {
            "department": None,
            "status": "needs_clarification",
        }

    return {
        "department": selected_department,
        "status": "routed",
    }
