# AI Recruitment Workflow Automation Agent

A deployment-ready Streamlit application that screens a PDF resume against a pasted job description using PyMuPDF for extraction and the Gemini API for structured resume analysis.

## Features

- PDF resume upload
- Job description input
- Resume text extraction with PyMuPDF
- Gemini-powered structured analysis
- Match score from 0 to 100
- Matching skills and missing skills
- Candidate summary and recommendation
- Deterministic decision engine:
  - Score > 85: Shortlist
  - Score 60-85: Escalate to HR Review
  - Score < 60: Reject
- Clear reasoning behind decisions
- Failure handling for empty PDFs, corrupted PDFs, missing job descriptions, missing API keys, and invalid AI responses

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
`-- utils
    |-- __init__.py
    |-- pdf_parser.py
    |-- prompts.py
    `-- scoring.py
```

## Local Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Set your Gemini API key.

```bash
set GEMINI_API_KEY=your_api_key_here
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

4. Run the app.

```bash
streamlit run app.py
```

## Streamlit Cloud Deployment

1. Push this project to GitHub.
2. Create a new Streamlit Cloud app from the repository.
3. Add this secret in Streamlit Cloud:

```toml
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-3.5-flash"
```

4. Set `app.py` as the entrypoint.

## Notes

- The app uses Gemini structured JSON output and validates the response before rendering results.
- The decision engine is deterministic and always uses the assignment thresholds, even when Gemini provides narrative recommendations.
- Scanned image-only resumes may return empty extracted text unless OCR is applied before upload.

## Disclaimer

This project is for internship assignment and workflow automation demonstration purposes. Human review is recommended before making real hiring decisions.
