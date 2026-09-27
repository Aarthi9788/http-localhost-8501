import os
from datetime import date

import requests
import streamlit as st


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


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


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.subtitle {
    font-size: 18px;
    color: #64748b;
}

.hero {
    padding: 28px;
    border-radius: 20px;
    background:
        linear-gradient(
            135deg,
            #0f172a,
            #1e3a5f
        );
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    margin-bottom: 5px;
}

.hero p {
    color: #dbeafe;
}

.preview {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 25px;
    min-height: 350px;
    white-space: pre-wrap;
    font-family:
        Georgia,
        "Times New Roman",
        serif;
    line-height: 1.7;
}

.notice {
    padding: 15px;
    border-radius: 10px;
    background: #fff7ed;
    border-left: 5px solid #f97316;
    margin-bottom: 15px;
}

.success-box {
    padding: 15px;
    border-radius: 10px;
    background: #ecfdf5;
    border-left: 5px solid #10b981;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "document" not in st.session_state:

    st.session_state.document = ""


if "source" not in st.session_state:

    st.session_state.source = ""


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="hero">

<h1>⚖️ LegalEase</h1>

<p>
AI-Powered Legal Document Generator
</p>

<p>
Create • Review • Edit • Download
</p>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚖️ LegalEase")

    st.write(
        "Generate professional "
        "AI-assisted legal drafts."
    )

    st.divider()

    st.subheader("Workflow")

    st.write(
        """
1. Select document type
2. Enter parties
3. Add terms
4. Choose effective date
5. Generate
6. Review
7. Edit
8. Download
"""
    )

    st.divider()

    st.caption(
        f"Backend: {BACKEND_URL}"
    )


# =========================================================
# COLUMNS
# =========================================================

left, right = st.columns(
    [1, 1.15],
    gap="large"
)


# =========================================================
# INPUT SECTION
# =========================================================

with left:

    st.subheader(
        "📝 1. Document Information"
    )

    document_type = st.selectbox(
        "Document Type",
        DOCUMENT_TYPES
    )

    parties = st.text_area(
        "Parties Involved",

        placeholder=(
            "Example:\n"
            "John Doe - Employee\n"
            "ABC Technologies Pvt Ltd - Employer"
        ),

        height=130
    )

    terms = st.text_area(
        "Terms & Conditions",

        placeholder=(
            "Example:\n"
            "Salary: ₹30,000 per month; "
            "Working hours: 9 AM to 5 PM; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 30 days notice"
        ),

        height=180
    )

    effective_date = st.date_input(
        "Effective Date",
        value=date.today()
    )

    jurisdiction = st.text_input(
        "Jurisdiction",

        placeholder=(
            "Example: Tamil Nadu, India"
        )
    )

    additional_instructions = st.text_area(
        "Additional Instructions",

        placeholder=(
            "Example: Use numbered clauses "
            "and include detailed signature sections."
        ),

        height=110
    )

    generate_button = st.button(
        "✨ Generate Legal Document",
        type="primary",
        use_container_width=True
    )


# =========================================================
# GENERATION
# =========================================================

if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "effective_date":
                effective_date.isoformat(),

            "jurisdiction":
                jurisdiction,

            "additional_instructions":
                additional_instructions,
        }

        with st.spinner(
            "🤖 Gemini is generating your document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=300
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.document = (
                    result["document"]
                )

                st.session_state.source = (
                    result["source"]
                )

                st.rerun()

            except requests.exceptions.RequestException as error:

                st.error(
                    "Could not connect to the "
                    f"backend.\n\n{error}"
                )


# =========================================================
# PREVIEW / EDIT
# =========================================================

with right:

    st.subheader(
        "📄 2. Preview & Edit"
    )

    if not st.session_state.document:

        st.info(
            "Your generated document will "
            "appear here."
        )

    else:

        if (
            st.session_state.source
            == "demo"
        ):

            st.markdown(
                """
<div class="notice">

<strong>Demo Mode</strong><br>

Gemini API key is not configured.
The application is currently using
a local demo generator.

Add your Gemini API key to the
<code>.env</code> file for real AI generation.

</div>
""",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
<div class="success-box">

<strong>Gemini AI Generated</strong><br>

Review the generated document carefully
before using it.

</div>
""",
                unsafe_allow_html=True
            )

        st.text_area(
            "Editable Document",

            key="document",

            height=520
        )


# =========================================================
# DOWNLOADS
# =========================================================

if st.session_state.document:

    st.divider()

    st.subheader(
        "⬇️ 3. Download Document"
    )

    col1, col2, col3 = st.columns(3)


    # -----------------------------------------------------
    # TXT
    # -----------------------------------------------------

    with col1:

        st.download_button(

            "📄 Download TXT",

            data=(
                st.session_state.document
                .encode("utf-8")
            ),

            file_name=(
                "legalease_document.txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


    # -----------------------------------------------------
    # DOCX
    # -----------------------------------------------------

    with col2:

        if st.button(
            "📝 Prepare DOCX",
            use_container_width=True
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/export/docx",

                    json={
                        "text":
                            st.session_state.document,

                        "document_type":
                            document_type,

                        "terms":
                            terms,
                    },

                    timeout=60
                )

                response.raise_for_status()

                st.session_state.docx_data = (
                    response.content
                )

            except Exception as error:

                st.error(
                    f"DOCX export failed: {error}"
                )


        if "docx_data" in st.session_state:

            st.download_button(

                "⬇️ Download DOCX",

                data=(
                    st.session_state.docx_data
                ),

                file_name=(
                    "legalease_document.docx"
                ),

                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),

                use_container_width=True
            )


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    with col3:

        if st.button(
            "📕 Prepare PDF",
            use_container_width=True
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/export/pdf",

                    json={
                        "text":
                            st.session_state.document,

                        "document_type":
                            document_type,
                    },

                    timeout=60
                )

                response.raise_for_status()

                st.session_state.pdf_data = (
                    response.content
                )

            except Exception as error:

                st.error(
                    f"PDF export failed: {error}"
                )


        if "pdf_data" in st.session_state:

            st.download_button(

                "⬇️ Download PDF",

                data=(
                    st.session_state.pdf_data
                ),

                file_name=(
                    "legalease_document.pdf"
                ),

                mime="application/pdf",

                use_container_width=True
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "LegalEase | AI-assisted legal drafting system"
)

st.caption(
    "AI-generated drafts should be reviewed "
    "by a qualified legal professional before "
    "being used for legally significant purposes."
)