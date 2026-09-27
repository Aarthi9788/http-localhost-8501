from io import BytesIO
import traceback

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.ai_generator import GeminiDocumentGenerator
from app.config import get_settings
from app.schemas import (
    DOCUMENT_TYPES,
    DocumentRequest,
    DocumentResponse,
    ExportRequest,
)
from app.services import (
    build_docx,
    build_pdf,
)
from app.utils import sanitize_text


router = APIRouter()

settings = get_settings()

generator = GeminiDocumentGenerator(
    settings
)


@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "LegalEase"
    }


@router.get("/document-types")
def document_types():

    return {
        "document_types": DOCUMENT_TYPES
    }


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        result = generator.generate_document(
            request
        )

        return DocumentResponse(
            document=result.text,
            document_type=request.document_type,
            source=result.source,
            model=result.model
        )

    except Exception as error:
        print("\n===== LEGAL EASE GENERATION ERROR =====")
        print(error)
        import traceback
        traceback.print_exc()
        print("=======================================\n")

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {error}"
        )


@router.post("/export/txt")
def export_txt(
    request: ExportRequest
):

    text = sanitize_text(
        request.text
    )

    return StreamingResponse(
        iter([text.encode("utf-8")]),
        media_type="text/plain",
        headers={
            "Content-Disposition":
            'attachment; filename="legalease_document.txt"'
        }
    )


@router.post("/export/docx")
def export_docx(
    request: ExportRequest
):

    try:

        data = build_docx(
            text=sanitize_text(
                request.text
            ),
            document_type=request.document_type,
            terms=request.terms
        )

        return StreamingResponse(
            BytesIO(data),
            media_type=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            headers={
                "Content-Disposition":
                'attachment; filename="legalease_document.docx"'
            }
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"DOCX export failed: {error}"
        )


@router.post("/export/pdf")
def export_pdf(
    request: ExportRequest
):

    try:

        data = build_pdf(
            text=sanitize_text(
                request.text
            ),
            document_type=request.document_type
        )

        return StreamingResponse(
            BytesIO(data),
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                'attachment; filename="legalease_document.pdf"'
            }
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed: {error}"
        )