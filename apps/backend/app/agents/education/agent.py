
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.agents.education.prompts import EDUCATION_SYSTEM_PROMPT
from app.agents.education.schema import EducationDetails
from app.core.llm import get_llm
from app.orchestration.state import ConcernState


DEPARTMENT = "education"
REQUIRED_FIELDS = ("issue", "school_name", "location")


def get_latest_user_message(messages: list) -> str | None:
    """Find the most recent message sent by the citizen."""
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return str(message.content)

    return None


def get_missing_fields(details: dict) -> list[str]:
    """Identify required education details that are still missing."""
    return [
        field
        for field in REQUIRED_FIELDS
        if not details.get(field)
    ]


def build_response(
    reply: str,
    details: dict,
    missing_fields: list[str],
    status: str,
) -> dict:
    """Build a consistent state update for the Education Agent."""
    return {
        "messages": [AIMessage(content=reply)],
        "department": DEPARTMENT,
        "extracted_details": details,
        "missing_fields": missing_fields,
        "status": status,
    }


def format_education_summary(details: dict) -> str:
    """Present the collected details for citizen confirmation."""
    return (
        "Here are your education concern details:\n\n"
        f"Issue: {details.get('issue')}\n"
        f"School: {details.get('school_name')}\n"
        f"Location: {details.get('location')}\n\n"
        "Are these details correct? Please answer Yes or No."
    )


def extract_education_details(messages: list) -> EducationDetails:
    """Extract education information from the conversation."""
    structured_llm = get_llm().with_structured_output(
        EducationDetails
    )

    return structured_llm.invoke([
        SystemMessage(
            content=(
                "Extract education concern details from the conversation. "
                "Use only information provided by the citizen. "
                "Do not invent missing information. "
                "Return None for unknown fields. "
                "school_name is the name of the school. "
                "location is the village, town, or city where the "
                "school is located. "
                "Do not copy the school name into the location field."
            )
        ),
        *messages,
    ])


def check_confirmation(messages: list) -> str:
    """Determine whether the citizen confirms the collected details."""
    latest_message = get_latest_user_message(messages)

    if latest_message is None:
        return "unclear"

    user_text = latest_message.strip().lower()

    positive_responses = {
        "yes",
        "yes.",
        "yes, correct",
        "yes, that's correct",
        "yes, that is correct",
        "yes, the information is correct",
        "yes, the information is correct. i confirm these details.",
        "correct",
        "confirmed",
        "i confirm",
        "i confirm these details",
        "that's correct",
        "that is correct",
    }

    negative_responses = {
        "no",
        "no.",
        "no, that's incorrect",
        "no, that is incorrect",
        "no, the location is incorrect",
        "incorrect",
        "not correct",
        "i want to correct something",
    }

    if user_text in positive_responses:
        return "yes"

    if user_text in negative_responses:
        return "no"

    # Use the LLM when the response is not a simple Yes or No.
    response = get_llm().invoke([
        SystemMessage(
            content=(
                "Classify the citizen's response to a request "
                "to confirm collected information. "
                "Return exactly one word: yes, no, or unclear. "
                "yes means the citizen approves the information. "
                "no means the citizen rejects or wants to correct it. "
                "unclear means neither is established. "
                "Do not return explanations."
            )
        ),
        HumanMessage(content=latest_message),
    ])

    answer = str(response.content).strip().lower().strip(" .!\"'")

    if answer in {"yes", "no", "unclear"}:
        return answer

    if answer.startswith("yes"):
        return "yes"

    if answer.startswith("no"):
        return "no"

    return "unclear"


def apply_education_correction(
    messages: list,
    saved_details: dict,
) -> EducationDetails:
    """Update only the information corrected by the citizen."""
    latest_message = get_latest_user_message(messages)

    if latest_message is None:
        return EducationDetails(**saved_details)

    structured_llm = get_llm().with_structured_output(
        EducationDetails
    )

    return structured_llm.invoke([
        SystemMessage(
            content=(
                "Update the existing education concern details "
                "using the citizen's latest correction. "
                "Preserve existing fields unless the citizen "
                "explicitly changes them. "
                "Use only information provided by the citizen. "
                "Do not invent information. "
                "Return the complete updated record."
            )
        ),
        HumanMessage(
            content=(
                f"Existing details: {saved_details}\n"
                f"Citizen's correction: {latest_message}"
            )
        ),
    ])


def ask_for_missing_details(
    messages: list,
    details: dict,
    missing_fields: list[str],
) -> str:
    """Ask the citizen for one missing required field."""
    response = get_llm().invoke([
        SystemMessage(
            content=(
                EDUCATION_SYSTEM_PROMPT
                + "\n\nCollected information:\n"
                + str(details)
                + "\n\nMissing required fields:\n"
                + str(missing_fields)
                + "\n\nAsk exactly ONE question about "
                "the first missing required field. "
                "Do not ask for optional details yet."
            )
        ),
        *messages,
    ])

    return str(response.content)


def handle_confirmation(state: ConcernState) -> dict:
    """Process a citizen's response to the confirmation question."""
    messages = state.get("messages", [])
    saved_details = state.get("extracted_details", {})
    saved_missing = state.get("missing_fields", [])

    answer = check_confirmation(messages)

    if answer == "yes":
        missing_fields = get_missing_fields(saved_details)

        if missing_fields:
            return build_response(
                reply=(
                    "Some required information is missing. "
                    f"Please provide the missing {missing_fields[0]}."
                ),
                details=saved_details,
                missing_fields=missing_fields,
                status="collecting_details",
            )

        return build_response(
            reply=(
                "Thank you. Your education concern details "
                "have been confirmed. "
                "No complaint has been submitted yet."
            ),
            details=saved_details,
            missing_fields=[],
            status="confirmed",
        )

    if answer == "no":
        return build_response(
            reply="Understood. What information would you like to correct?",
            details=saved_details,
            missing_fields=saved_missing,
            status="awaiting_correction",
        )

    return build_response(
        reply=(
            "Please confirm whether the collected information "
            "is correct. Reply Yes or No."
        ),
        details=saved_details,
        missing_fields=saved_missing,
        status="awaiting_confirmation",
    )


def handle_correction(state: ConcernState) -> dict:
    """Apply a correction and check whether details are complete."""
    saved_details = state.get("extracted_details", {})

    corrected = apply_education_correction(
        state.get("messages", []),
        saved_details,
    )

    updated_details = corrected.model_dump()
    missing_fields = get_missing_fields(updated_details)

    if missing_fields:
        return build_response(
            reply=(
                "Thank you for the correction. "
                f"Please provide the missing {missing_fields[0]}."
            ),
            details=updated_details,
            missing_fields=missing_fields,
            status="collecting_details",
        )

    return build_response(
        reply=format_education_summary(updated_details),
        details=updated_details,
        missing_fields=[],
        status="awaiting_confirmation",
    )


def collect_education_details(state: ConcernState) -> dict:
    """Extract details and decide what information to request next."""
    messages = state.get("messages", [])

    details = extract_education_details(messages)
    extracted_details = details.model_dump()
    missing_fields = get_missing_fields(extracted_details)

    if missing_fields:
        reply = ask_for_missing_details(
            messages,
            extracted_details,
            missing_fields,
        )
        status = "collecting_details"
    else:
        reply = format_education_summary(extracted_details)
        status = "awaiting_confirmation"

    return build_response(
        reply=reply,
        details=extracted_details,
        missing_fields=missing_fields,
        status=status,
    )


def education_agent(state: ConcernState) -> dict:
    """
    Manage an education concern conversation.

    Collect required details, handle citizen corrections,
    and confirm the information before any future submission.
    """
    current_status = state.get("status")

    if current_status == "confirmed":
        return build_response(
            reply=(
                "These education concern details have already "
                "been confirmed. Please start a new conversation "
                "for a different concern."
            ),
            details=state.get("extracted_details", {}),
            missing_fields=[],
            status="confirmed",
        )

    if current_status == "awaiting_confirmation":
        return handle_confirmation(state)

    if current_status == "awaiting_correction":
        return handle_correction(state)

    return collect_education_details(state)
