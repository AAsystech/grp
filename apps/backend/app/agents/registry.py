
from typing import TypedDict


class AgentInfo(TypedDict):
    """Information used by the Supervisor to identify a department."""

    name: str
    description: str


# Central registry of departments supported by the application.
AGENT_REGISTRY: dict[str, AgentInfo] = {
    "education": {
        "name": "Education Agent",
        "description": (
            "Handles education-related concerns, including "
            "school facilities, classrooms, and infrastructure."
        ),
    },
    "gram_panchayat": {
        "name": "Gram Panchayat Agent",
        "description": (
            "Handles village-level concerns, including "
            "streetlights, roads, drainage, sanitation, "
            "and drinking water supply."
        ),
    },
}


def get_available_agents() -> dict[str, AgentInfo]:
    """Return the departments available for Supervisor routing."""
    return AGENT_REGISTRY
