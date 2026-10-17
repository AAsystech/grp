
from pydantic import BaseModel, Field


class GramPanchayatDetails(BaseModel):
    """
    Structured information collected for a Gram Panchayat concern.

    Required information:
    - issue
    - village_name
    - location

    Optional information:
    - additional_details
    """

    issue: str | None = Field(
        default=None,
        description="Description of the village-related problem reported by the citizen.",
    )

    village_name: str | None = Field(
        default=None,
        description="Name of the village affected by the concern.",
    )

    location: str | None = Field(
        default=None,
        description="Specific location or nearby landmark within the village.",
    )

    additional_details: str | None = Field(
        default=None,
        description="Any additional relevant information provided by the citizen.",
    )
