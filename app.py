from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()
import streamlit as st

import os

from utils.pdf_parser import CorruptedPDFError, EmptyPDFError, extract_text_from_pdf
from utils.scoring import (
    InvalidAIResponseError,
    MissingAPIKeyError,
    analyze_resume_with_gemini,
    make_decision,
)


st.set_page_config(
    page_title="AI Recruitment Workflow Automation Agent",
    page_icon=":material/work:",
    layout="wide",
)


def get_secret(name: str) -> str | None:
    """Read configuration from Streamlit secrets first, then environment variables."""

    try:
        return st.secrets.get(name) or os.getenv(name)
    except Exception:
        return os.getenv(name)


def render_header() -> None:
    st.title("AI Recruitment Workflow Automation Agent")
    st.caption(
        "Upload a resume, paste a job description, and generate a structured screening decision."
    )


def render_score(score: int) -> None:
    st.metric("Match Score", f"{score}/100")
    st.progress(score / 100)


def render_list(title: str, items: list[str], empty_message: str) -> None:
    st.subheader(title)
    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.info(empty_message)


def main() -> None:
    render_header()

    with st.sidebar:
        st.header("Configuration")

        theme_mode = st.radio(
            "Theme Mode",
            ["Dark", "Light"],
            index=0,
        )

        if theme_mode == "Light":
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: white;
                    color: black;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

        model_name = st.text_input(
            "Gemini model",
            value=get_secret("GEMINI_MODEL") or "gemini-2.5-flash",
        )
        st.caption("Set `GEMINI_API_KEY` in Streamlit Cloud secrets before deployment.")

    left, right = st.columns([1, 1], gap="large")

    with left:
        uploaded_resume = st.file_uploader("Upload PDF resume", type=["pdf"])

    with right:
        job_description = st.text_area(
            "Paste Job Description",
            height=260,
            placeholder="Paste the role responsibilities, required skills, and qualifications here...",
        )

    analyze_clicked = st.button("Analyze Resume", type="primary", use_container_width=True)

    if not analyze_clicked:
        st.info("Provide a PDF resume and job description, then run the analysis.")
        return

    if uploaded_resume is None:
        st.error("Please upload a PDF resume before analysis.")
        return

    if not job_description.strip():
        st.error("Missing Job Description. Please paste a job description before analysis.")
        return

    # Parse the resume before calling Gemini so PDF problems fail fast and clearly.
    try:
        parsed_resume = extract_text_from_pdf(uploaded_resume)
    except EmptyPDFError as exc:
        st.error(str(exc))
        return
    except CorruptedPDFError as exc:
        st.error(str(exc))
        return

    api_key = get_secret("GEMINI_API_KEY")
    try:
        with st.spinner("Analyzing candidate with Gemini..."):
            analysis = analyze_resume_with_gemini(
                resume_text=parsed_resume.text,
                job_description=job_description,
                api_key=api_key,
                model_name=model_name,
            )

        decision = make_decision(analysis.match_score)

    except MissingAPIKeyError as exc:
        st.error(str(exc))
        return

    except InvalidAIResponseError as exc:
        st.error(str(exc))
        return

    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        return

    st.divider()

    score_col, decision_col = st.columns([1, 1])

    with score_col:
        render_score(analysis.match_score)

    with decision_col:
        st.subheader("Recommendation")
        st.success(analysis.recommendation)

    summary_col, reasoning_col = st.columns([1, 1], gap="large")

    with summary_col:
        st.subheader("Candidate Summary")
        st.write(analysis.candidate_summary)

    with reasoning_col:
        st.subheader("Decision Reasoning")
        st.write(analysis.decision_reasoning)

    skills_col, missing_col = st.columns([1, 1], gap="large")

    with skills_col:
        render_list(
            "Matching Skills",
            analysis.matching_skills,
            "No matching skills identified.",
        )

    with missing_col:
        render_list(
            "Missing Skills",
            analysis.missing_skills,
            "No missing skills identified.",
        )


if __name__ == "__main__":
    main()

st.divider()
st.caption("Built by Muhammad Anas Sajid • AI Recruitment Workflow Automation Agent")