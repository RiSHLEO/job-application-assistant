![CI](https://github.com/RiSHLEO/job-application-assistant/actions/workflows/ci.yml/badge.svg)

# Job Application Assistant

A production-grade AI system that analyses your CV against any job description 
and returns a match score, skill gaps, rewritten CV sections, and a tailored 
cover letter — all powered by GPT-3.5-turbo.

**Live App:** [Click here](your-streamlit-url)  
**API Docs:** [Swagger UI](your-render-url/docs)

---

## How It Works

CV (PDF) + Job Description
↓
FastAPI backend receives and validates input
↓
pypdf extracts text from CV
↓
GPT-3.5-turbo-16k analyses match and generates structured JSON
↓
Pydantic validates the response
↓
Streamlit frontend displays results

---

## API Endpoints

**GET /health**
Returns API status and version. Used for health monitoring and deployment verification.

**POST /analyse**
Accepts a CV as a PDF file and job description as form text.
Returns structured JSON containing:
- Match score (0-100)
- Match summary
- Key strengths
- Skill gaps with importance rating and how to address each
- CV section rewrites tailored to the job
- Complete cover letter

**GET /docs**
Auto-generated Swagger UI documentation built from Pydantic models.

---

## Technical Stack

- **API Framework:** FastAPI with Pydantic data validation
- **LLM:** GPT-3.5-turbo-16k via OpenAI API
- **PDF Processing:** pypdf
- **Frontend:** Streamlit
- **Containerisation:** Docker
- **CI/CD:** GitHub Actions
- **Backend Deployment:** Render
- **Frontend Deployment:** Streamlit Cloud

---
---

## How to Run Locally

**Without Docker:**
```bash
git clone https://github.com/RiSHLEO/job-application-assistant
cd job-application-assistant
pip install -r requirements.txt
```

Create a `.env` file: OPENAI_API_KEY=your-key-here

Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

Start the frontend in a separate terminal:
```bash
cd frontend
streamlit run app.py
```

**With Docker:**
```bash
docker build -t job-application-assistant .
docker run -p 8000:8000 --env-file .env job-application-assistant
```

Then run the frontend separately:
```bash
cd frontend
streamlit run app.py
```

---

## Running the Tests

```bash
pytest tests/ -v
```

Six tests covering:
- Health endpoint returns correct status
- Rejects non-PDF file uploads
- Rejects short job descriptions
- Rejects missing CV
- Rejects missing job description

---

## CI/CD Pipeline

GitHub Actions runs the full test suite automatically on every push to main. 
If any test fails, the pipeline stops and GitHub notifies you before broken 
code can reach production.

Pipeline steps:
1. Checkout code
2. Set up Python 3.11
3. Install dependencies
4. Run pytest

---

## What I Would Improve With More Time

- Deploy backend to AWS Elastic Beanstalk with auto-scaling
- Add streaming — show GPT response token by token as it generates
- Add LLM evaluation using RAGAS to measure response quality
- Store analysis history in a database so users can review past applications
- Add authentication so users have private accounts
- Support DOCX files in addition to PDF
- Add a bulk analysis mode — analyse one CV against multiple job descriptions simultaneously