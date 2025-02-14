# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Question(BaseModel):
    id: str
    category: str
    difficulty: str
    question: str
    expected_keywords: List[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "q1",
                "category": "python",
                "difficulty": "intermediate",
                "question": "Explain decorators in Python",
                "expected_keywords": ["wrapper", "function", "decorator", "@syntax"]
            }
        }
    }

@router.get("/questions/{category}", 
           response_model=List[Question],
           tags=["Questions"])
async def get_questions(category: str):
    """Get questions by category"""
    # Mock response for now
    return [
        {
            "id": "q1",
            "category": category,
            "difficulty": "intermediate",
            "question": "Sample question",
            "expected_keywords": ["keyword1", "keyword2"]
        }
    ] 