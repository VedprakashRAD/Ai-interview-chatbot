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

@router.get("/questions/{domain}/{skill_level}",
           response_model=List[Question])
async def get_questions(domain: str, skill_level: str):
    """Get 15 questions based on domain and skill level"""
    try:
        question_service = QuestionService()
        questions = question_service.get_questions_for_interview(domain, skill_level)
        return questions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 