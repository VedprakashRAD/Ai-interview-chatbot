# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

class EvaluationResponse(BaseModel):
    score: float
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

@router.post("/evaluation/evaluate",
            response_model=EvaluationResponse,
            tags=["Evaluation"])
async def evaluate_answers(answers: List[dict]):
    """Evaluate interview answers"""
    # Mock response for now
    return {
        "score": 8.5,
        "feedback": "Good performance",
        "strengths": ["Technical knowledge"],
        "weaknesses": ["Need more examples"],
        "recommendations": ["Practice more"]
    } 