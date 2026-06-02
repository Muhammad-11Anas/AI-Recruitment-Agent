# AI Recruitment Workflow Automation Agent

A deployment-ready Streamlit application that automates resume screening by comparing uploaded PDF resumes against job descriptions using AI-powered analysis with the Gemini API.

---

## Features

* PDF resume upload
* Job description input
* Resume text extraction using PyMuPDF
* AI-powered structured resume analysis
* Match score generation (0–100)
* Matching skills detection
* Missing skills identification
* Candidate summary generation
* Recommendation system
* Deterministic hiring decision engine:

  * Score > 85 → Shortlist
  * Score 60–85 → Escalate to HR Review
  * Score < 60 → Reject
* Explainable decision reasoning
* Dark and Light mode support
* Error handling for:

  * Empty PDFs
  * Corrupted PDFs
  * Missing job descriptions
  * Missing API keys
  * Invalid AI responses
  * Invalid JSON outputs

---

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

---

## Technologies Used

* Python
* Streamlit
* Gemini API
* PyMuPDF
* Pydantic
* Git & GitHub

---

## Local Setup

### 1. Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Gemini API Key

Command Prompt:

```bash
set GEMINI_API_KEY=your_api_key_here
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

---

### 4. Run the application

```bash
streamlit run app.py
```

---

## Streamlit Cloud Deployment

1. Push project to GitHub.
2. Create a Streamlit Cloud application.
3. Connect the GitHub repository.
4. Add the following secrets:

```toml
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-1.5-flash-latest"
```

5. Set `app.py` as the main entry point.

---

## System Workflow

1. User uploads PDF resume.
2. User pastes job description.
3. Resume text is extracted.
4. Gemini API analyzes resume against the job description.
5. System generates:

   * Match score
   * Matching skills
   * Missing skills
   * Candidate summary
   * Recommendation
   * Decision reasoning
6. Deterministic decision engine generates final hiring decision.

---

## Example Use Cases

* AI/ML internship screening
* Software engineering recruitment automation
* Resume shortlisting workflows
* HR screening assistance
* Recruitment process demonstration

---

## GitHub Repository

https://github.com/Muhammad-11Anas/AI-Recruitment-Agent

---

## Notes

* The system validates Gemini responses before rendering output.
* Structured JSON validation improves reliability and stability.
* The hiring decision engine is deterministic and independent from AI narrative recommendations.
* Scanned image-based resumes may require OCR preprocessing.

---

## Disclaimer

This project is developed for educational, research, and workflow automation demonstration purposes. Human review is recommended before making actual hiring decisions.
