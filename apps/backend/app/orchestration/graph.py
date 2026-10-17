
from langgraph.graph import START, END, StateGraph

from app.agents.supervisor.agent import supervisor_agent
from app.agents.education.agent import education_agent
from app.agents.gram_panchayat.agent import gram_panchayat_agent
from app.orchestration.state import ConcernState


# Departments currently supported by the workflow.
DEPARTMENTS = ("education", "gram_panchayat")


def route_at_start(state: ConcernState) -> str:
    """
    Decide where a conversation should begin.

    New conversations go to the Supervisor.
    Existing conversations continue with their assigned department.
    """
    department = state.get("department")

    if department in DEPARTMENTS:
        return department

    return "supervisor"


def route_to_department(state: ConcernState) -> str:
    """
    Route the Supervisor's decision to a department.

    End the workflow if the Supervisor cannot identify
    a supported department.
    """
    department = state.get("department")

    if department in DEPARTMENTS:
        return department

    return "end"


def create_concern_graph():
    """Build and compile the citizen concern workflow."""

    workflow = StateGraph(ConcernState)

    # Register the Supervisor and department agents.
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("education", education_agent)
    workflow.add_node("gram_panchayat", gram_panchayat_agent)

    # New conversations start with the Supervisor.
    # Existing conversations continue with their department.
    workflow.add_conditional_edges(
        START,
        route_at_start,
        {
            "supervisor": "supervisor",
            "education": "education",
            "gram_panchayat": "gram_panchayat",
        },
    )

    # The Supervisor selects which department handles the concern.
    workflow.add_conditional_edges(
        "supervisor",
        route_to_department,
        {
            "education": "education",
            "gram_panchayat": "gram_panchayat",
            "end": END,
        },
    )

    # Each department finishes after responding to the citizen.
    workflow.add_edge("education", END)
    workflow.add_edge("gram_panchayat", END)

    return workflow.compile()


# Compiled graph used by the FastAPI chat endpoint.
concern_graph = create_concern_graph()
