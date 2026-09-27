from datetime import date

from pydantic import BaseModel, Field, field_validator


DOCUMENT_TYPES = [
    "Employment Contract",
    "Non-Disclosure Agreement",
    "Lease Agreement",
    "Service Agreement",
    "Freelance Work Contract",
    "Employment Offer Letter",
    "General Agreement",
    "Custom Legal Document",
]


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=3,
        max_length=4000
    )

    terms: str = Field(
        ...,
        min_length=3,
        max_length=8000
    )

    effective_date: date

    jurisdiction: str = Field(
        default="",
        max_length=500
    )

    additional_instructions: str = Field(
        default="",
        max_length=4000
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "jurisdiction",
        "additional_instructions"
    )
    @classmethod
    def clean_text(cls, value: str) -> str:
        return value.strip()


class DocumentResponse(BaseModel):
    document: str
    document_type: str
    source: str
    model: str


class ExportRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )

    document_type: str = Field(
        default="Legal Document",
        max_length=120
    )

    terms: str = Field(
        default="",
        max_length=8000
    )