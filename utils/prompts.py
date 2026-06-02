from __future__ import annotations


ANALYSIS_SYSTEM_INSTRUCTION = """
You are an expert technical recruiter and HR screening assistant.
Evaluate only the resume content against the provided job description.
Be fair, evidence-based, and concise. Do not invent experience or skills.
"""


def build_resume_analysis_prompt(resume_text: str, job_description: str) -> str:
    """Build the prompt sent to Gemini for resume-to-job analysis."""

    return f"""
Analyze the candidate resume against the job description.

Return a strict JSON object that matches the provided schema.

Scoring guidance:
- 90-100: Excellent alignment across required skills, experience, and responsibilities.
- 75-89: Strong alignment with minor gaps.
- 60-74: Partial alignment; plausible candidate but needs HR validation.
- 40-59: Weak alignment; several important gaps.
- 0-39: Poor alignment or unrelated background.

Focus on:
- Required and preferred skills.
- Relevant experience and projects.
- Education/certifications if relevant.
- Evidence present in the resume.
- Important missing requirements from the job description.

Resume:
\"\"\"{resume_text[:18000]}\"\"\"

Job Description:
\"\"\"{job_description[:9000]}\"\"\"
"""
