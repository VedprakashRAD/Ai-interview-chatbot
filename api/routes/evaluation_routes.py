# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class EvaluationResponse(BaseModel):
    score: float  # Score out of 100
    feedback: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "score": 8.5,
                "feedback": "Good performance overall",
                "strengths": ["Technical knowledge", "Clear communication"],
                "weaknesses": ["Could improve on specific examples"],
                "recommendations": ["Practice more system design questions"]
            }
        }
    }

@router.post("/evaluation/evaluate")
async def evaluate_answers(answers: List[dict]):
    """Evaluate answers and return score out of 100"""
    evaluation_service = EvaluationService()
    result = evaluation_service.evaluate_answers(answers)
    
    # Convert score to 100-point scale
    result['score'] = result['score'] * 100
    
    return result 