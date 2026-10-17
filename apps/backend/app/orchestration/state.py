
from typing import Any

from typing_extensions import NotRequired
from langgraph.graph import MessagesState


class ConcernState(MessagesState):
    """
    Shared conversation state used by the Supervisor
    and department agents.

    MessagesState automatically manages conversation messages.
    The additional fields track department selection,
    collected information, and conversation progress.
    """

    department: NotRequired[str | None]
    intent: NotRequired[str | None]
    extracted_details: NotRequired[dict[str, Any]]
    missing_fields: NotRequired[list[str]]
    status: NotRequired[str]
