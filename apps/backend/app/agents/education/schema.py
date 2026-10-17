
from pydantic import BaseModel, Field


class EducationDetails(BaseModel):
    """
    Structured information collected for an education concern.

    Required information:
    - issue
    - school_name
    - location

    Optional information:
    - additional_details
    """

    issue: str | None = Field(
        default=None,
        description="Description of the education-related problem or request.",
    )

    school_name: str | None = Field(
        default=None,
        description="Name of the school affected by the concern.",
    )

    location: str | None = Field(
        default=None,
        description="Village, town, or city where the school is located.",
    )

    additional_details: str | None = Field(
        default=None,
        description="Any additional relevant information provided by the citizen.",
    )
