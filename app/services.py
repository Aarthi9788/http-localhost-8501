from io import BytesIO
from pathlib import Path
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "logo.png"


def get_lines(text: str):

    return (
        text
        .replace("\r\n", "\n")
        .split("\n")
    )


# =========================================================
# DOCX
# =========================================================

def build_docx(
    text: str,
    document_type: str,
    terms: str = ""
) -> bytes:

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    normal_style = document.styles["Normal"]

    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)

    # Logo

    if LOGO_PATH.exists():

        paragraph = document.add_paragraph()

        paragraph.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER
        )

        run = paragraph.add_run()

        run.add_picture(
            str(LOGO_PATH),
            width=Inches(1.25)
        )

    # Title

    title = document.add_paragraph()

    title.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    title_run = title.add_run(
        document_type.upper()
    )

    title_run.bold = True

    title_run.font.size = Pt(15)

    # Body

    headings = {
        "PARTIES",
        "RECITALS",
        "TERMS AND CONDITIONS",
        "GENERAL PROVISIONS",
        "SIGNATURES",
        "DRAFTING NOTICE",
    }

    for line in get_lines(text):

        line = line.strip()

        if not line:

            document.add_paragraph()

            continue

        paragraph = document.add_paragraph()

        paragraph.paragraph_format.space_after = Pt(6)

        if line.upper() in headings:

            run = paragraph.add_run(
                line
            )

            run.bold = True

            run.font.size = Pt(12)

        else:

            paragraph.add_run(line)

    # Terms table

    term_list = [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]

    if term_list:

        document.add_page_break()

        heading = document.add_paragraph()

        heading_run = heading.add_run(
            "TERM SUMMARY"
        )

        heading_run.bold = True

        table = document.add_table(
            rows=1,
            cols=2
        )

        table.style = "Table Grid"

        table.rows[0].cells[0].text = "No."

        table.rows[0].cells[1].text = "Term"

        for index, term in enumerate(
            term_list,
            start=1
        ):

            cells = table.add_row().cells

            cells[0].text = str(index)

            cells[1].text = term

    # Footer

    footer = section.footer.paragraphs[0]

    footer.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer_run = footer.add_run(
        "LegalEase - AI-assisted draft. "
        "Review before legal use."
    )

    footer_run.italic = True

    output = BytesIO()

    document.save(output)

    return output.getvalue()


# =========================================================
# PDF
# =========================================================

class LegalEasePDF(FPDF):

    def __init__(
        self,
        document_type: str
    ):

        super().__init__()

        self.document_type = (
            document_type
        )

        self.set_auto_page_break(
            auto=True,
            margin=18
        )

    def header(self):

        if LOGO_PATH.exists():

            self.image(
                str(LOGO_PATH),
                x=92,
                y=8,
                w=26
            )

            self.ln(18)

        else:

            self.ln(8)

        self.set_font(
            "Helvetica",
            "B",
            11
        )

        self.cell(
            0,
            8,
            self.document_type.upper(),
            align="C"
        )

        self.ln(8)

    def footer(self):

        self.set_y(-14)

        self.set_font(
            "Helvetica",
            "I",
            8
        )

        self.cell(
            0,
            8,
            "LegalEase - AI-assisted draft. "
            "Review before legal use.",
            align="C"
        )


def build_pdf(
    text: str,
    document_type: str
) -> bytes:

    pdf = LegalEasePDF(
        document_type
    )

    pdf.set_margins(
        18,
        18,
        18
    )

    pdf.add_page()

    pdf.set_font(
        "Helvetica",
        size=10
    )

    headings = {
        "PARTIES",
        "RECITALS",
        "TERMS AND CONDITIONS",
        "GENERAL PROVISIONS",
        "SIGNATURES",
        "DRAFTING NOTICE",
    }

    for line in get_lines(text):

        line = line.strip()

        if not line:

            pdf.ln(4)

            continue

        # FPDF Helvetica is not Unicode-complete.
        safe_line = (
            line
            .encode(
                "latin-1",
                "replace"
            )
            .decode("latin-1")
        )

        if line.upper() in headings:

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                6,
                safe_line
            )

            pdf.set_font(
                "Helvetica",
                size=10
            )

        else:

            pdf.multi_cell(
                0,
                5.5,
                safe_line
            )

    return bytes(
        pdf.output()
    )