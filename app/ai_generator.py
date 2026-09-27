from dataclasses import dataclass

from google import genai

from app.config import Settings
from app.schemas import DocumentRequest


@dataclass
class GenerationResult:
    text: str
    source: str
    model: str


class GeminiDocumentGenerator:

    def __init__(self, settings: Settings):

        self.settings = settings
        self.client = None

        if settings.gemini_api_key:
            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    def build_prompt(
        self,
        request: DocumentRequest
    ) -> str:

        jurisdiction = (
            request.jurisdiction
            if request.jurisdiction
            else "Not specified"
        )

        instructions = (
            request.additional_instructions
            if request.additional_instructions
            else "None"
        )

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Your task is to create a professional DRAFT legal document.

DOCUMENT TYPE:
{request.document_type}

PARTIES:
{request.parties}

EFFECTIVE DATE:
{request.effective_date.isoformat()}

JURISDICTION:
{jurisdiction}

TERMS AND CONDITIONS:
{request.terms}

ADDITIONAL INSTRUCTIONS:
{instructions}

IMPORTANT RULES:

1. Use only facts supplied by the user.

2. Never invent:
   - names
   - addresses
   - money amounts
   - dates
   - registration numbers
   - statutes
   - case citations
   - obligations
   - legal authorities

3. If important information is missing, write:

[MISSING: describe required information]

4. Produce a professional legal-document draft.

5. Use a clear title.

6. Use numbered sections and clauses.

7. Include appropriate signature blocks.

8. Do not claim that the document is lawyer-reviewed.

9. Do not claim that the document is guaranteed legally valid.

10. Do not include Markdown code fences.

11. Include a short drafting notice at the end.

Return only the legal document.
"""

        return prompt.strip()

    def generate_document(
        self,
        request: DocumentRequest
    ) -> GenerationResult:

        # --------------------------------
        # DEMO MODE
        # --------------------------------

        if not self.client:

            return GenerationResult(
                text=self.demo_document(request),
                source="demo",
                model="demo-generator"
            )

        # --------------------------------
        # GEMINI GENERATION
        # --------------------------------

        response = self.client.models.generate_content(
            model=self.settings.gemini_model,
            contents=self.build_prompt(request)
        )

        generated_text = (
            response.text or ""
        ).strip()

        if not generated_text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return GenerationResult(
            text=generated_text,
            source="gemini",
            model=self.settings.gemini_model
        )

    @staticmethod
    def demo_document(
        request: DocumentRequest
    ) -> str:

        terms = [
            term.strip()
            for term in request.terms.split(";")
            if term.strip()
        ]

        if terms:

            numbered_terms = "\n".join(
                f"{index}. {term}"
                for index, term in enumerate(
                    terms,
                    start=1
                )
            )

        else:

            numbered_terms = (
                "1. [MISSING: Terms and Conditions]"
            )

        return f"""
DRAFT {request.document_type.upper()}

Effective Date:
{request.effective_date.isoformat()}


PARTIES

{request.parties}


RECITALS

The parties intend to enter into this
{request.document_type} on the Effective Date,
subject to the terms and conditions contained
in this document.


TERMS AND CONDITIONS

{numbered_terms}


GENERAL PROVISIONS

1. Entire Agreement

This draft represents the information supplied
by the user for document-generation purposes.

2. Amendments

Any amendment should be made in writing and
agreed to by the parties.

3. Severability

If any provision is found to be unenforceable,
the remaining provisions should remain effective
to the extent permitted by applicable law.

4. Governing Law

[MISSING: Specify governing law and jurisdiction.]


SIGNATURES

Party 1:

Name: ______________________________

Signature: _________________________

Date: ______________________________


Party 2:

Name: ______________________________

Signature: _________________________

Date: ______________________________


DRAFTING NOTICE

This document is an AI-assisted draft created
from the information supplied by the user.

It has not been reviewed by a qualified lawyer.
The document should be checked against the
applicable law, jurisdiction, facts and specific
transaction requirements before use.
""".strip()