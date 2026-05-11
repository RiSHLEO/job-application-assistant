from pydantic import BaseModel, Field
from typing import List

class AnalysisRequest(BaseModel):
    job_description: str = Field(..., min_length=50, description="The job description to analyse against")

class SkillGap(BaseModel):
    skill: str
    importance: str
    how_to_address: str

class CVSection(BaseModel):
    section_name: str
    original: str
    rewritten: str

class AnalysisResponse(BaseModel):
    match_score: int = Field(..., ge=0, le=100, description="Match percentage between CV and job description")
    match_summary: str
    skill_gaps: List[SkillGap]
    cv_improvements: List[CVSection]
    cover_letter: str
    key_strengths: List[str]

class HealthResponse(BaseModel):
    status: str
    version: str