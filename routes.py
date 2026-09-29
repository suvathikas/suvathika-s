from fastapi import APIRouter, HTTPException

from app.models import DocumentRequest, DocumentResponse
from app.generator import DISCLAIMER, generate_document


router = APIRouter(
    prefix="/api",
    tags=["Legal Documents"]
)


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate(request: DocumentRequest):
    """Generate a legal document draft."""

    try:
        document, source = generate_document(request)

        return DocumentResponse(
            document=document,
            source=source,
            disclaimer=DISCLAIMER
        )

    except Exception as exc:
        # Keep provider errors and sensitive details
        # out of the public API response.
        print(f"Document generation error: {exc}")

        raise HTTPException(
            status_code=502,
            detail=(
                "Document generation failed. "
                "Check the backend configuration "
                "and server logs."
            )
        ) from exc