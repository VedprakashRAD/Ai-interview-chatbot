# -*- coding: utf-8 -*-
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Dict, List
from pydantic import BaseModel
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Define response models
class ResumeResponse(BaseModel):
    skills: List[str]
    experience: List[str]
    education: List[str]

    model_config = {
        "json_schema_extra": {
            "example": {
                "skills": ["Python", "FastAPI", "Machine Learning"],
                "experience": ["Senior Developer", "Tech Lead"],
                "education": ["Master in Computer Science"]
            }
        }
    }

@router.post(
    "/resume/upload",
    response_model=ResumeResponse,
    status_code=200,
    description="Upload and parse a resume file"
)
async def upload_resume(
    file: UploadFile = File(...)  # ... means required
):
    """Upload and parse resume file"""
    try:
        logger.info(f"Received file: {file.filename}")
        
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        logger.debug(f"File content: {text[:100]}...")  # Log first 100 chars

        # Parse sections
        sections = parse_resume_text(text)
        
        logger.debug(f"Parsed sections: {sections}")
        
        # Create response
        response = ResumeResponse(
            skills=sections['skills'],
            experience=sections['experience'],
            education=sections['education']
        )
        
        logger.info("Successfully processed resume")
        return response

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

def parse_resume_text(text: str) -> Dict[str, List[str]]:
    """Parse resume text into sections"""
    sections = {
        'skills': [],
        'experience': [],
        'education': []
    }
    
    current_section = None
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        line_lower = line.lower()
        if 'skills' in line_lower:
            current_section = 'skills'
            continue
        elif 'experience' in line_lower:
            current_section = 'experience'
            continue
        elif 'education' in line_lower:
            current_section = 'education'
            continue
            
        # Add content to current section
        if current_section == 'skills':
            # Split skills by comma and clean them
            skills = [s.strip() for s in line.split(',')]
            sections['skills'].extend([s for s in skills if s])
        elif current_section in ['experience', 'education']:
            if line.strip():
                sections[current_section].append(line)
    
    # Ensure we have all required sections
    if not all(sections.values()):
        raise ValueError("Missing required sections in resume")
        
    return sections
            