from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import AnalysisResponse, HealthResponse
from analyzer import analyse_application
import json

# Create FastAPI app
app = FastAPI(
    title="Job Application Assistant API",
    description="AI-powered CV analysis and cover letter generation",
    version="1.0.0"
)

# CORS middleware - Cross Origin Resource Sharing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ============ ENDPOINTS ============

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )

@app.post("/analyse", response_model=AnalysisResponse)
async def analyse(
    cv: UploadFile = File(..., description="CV in PDF format"),
    job_description: str = Form(..., description="Job description text")
):
    # Validate file type
    if not cv.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )
    
    # Validate file size — max 5MB
    cv_bytes = await cv.read()
    if len(cv_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB"
        )
    
    # Validate job description length
    if len(job_description.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Job description too short. Please provide a complete job description."
        )
    
    try:
        # Run analysis
        result = analyse_application(cv_bytes, job_description)
        return AnalysisResponse(**result)
    
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Failed to parse AI response. Please try again."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )