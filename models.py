from typing import Literal

from pydantic import BaseModel, Field, field_validator


DocumentType = Literal[
    "Non-disclosure agreement",
    "Service agreement",
    "Rental agreement",
    "Employment offer letter",
    "Demand letter",
    "Custom document",
]


class DocumentRequest(BaseModel):
    document_type: DocumentType

    jurisdiction: str = Field(
        default="Not specified",
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        min_length=3,
        max_length=4000
    )

    terms: str = Field(
        min_length=3,
        max_length=8000
    )

    effective_date: str = Field(
        default="Not specified",
        max_length=100
    )

    duration: str = Field(
        default="Not specified",
        max_length=200
    )

    @field_validator("parties", "terms")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be blank.")
        return value.strip()


class DocumentResponse(BaseModel):
    document: str
    source: Literal["template", "llm"]
    disclaimer: str