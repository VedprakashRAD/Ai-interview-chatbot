from pydantic import BaseModel
from typing import List

class ResumeResponse(BaseModel):
    skills: List[str]
    experience: List[str]
    education: List[str]
    domain: str
    skill_level: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "experience": ["Senior Developer", "Tech Lead"],
                "education": ["Master in Computer Science"],
                "domain": "ai_ml",
                "skill_level": "intermediate"
            }
        }
    }
