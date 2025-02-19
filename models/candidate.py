from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class Domain(str, Enum):
    AI_ML = "AI/ML"
    WEB_DEV = "Web Development"
    SALES = "Sales"
    BUSINESS_ANALYST = "Business Analyst"
    MARKETING = "Marketing"

class Candidate(BaseModel):
    candidate_id: Optional[str] = None
    test_id: Optional[str] = None
    name: str
    father_name: str
    email: EmailStr
    domain: Domain
    resume_path: Optional[str] = None
    photo_path: Optional[str] = None
    parsed_resume_data: Optional[dict] = None 