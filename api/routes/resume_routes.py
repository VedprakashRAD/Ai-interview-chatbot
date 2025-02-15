# -*- coding: utf-8 -*-
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List
import logging
import os
from api.models.resume import ResumeResponse
from services.resume_service import ResumeService

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Define allowed file types
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}
ALLOWED_MIME_TYPES = {
    'application/pdf': '.pdf',
    'application/msword': '.doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
}

@router.post(
    "/resume/upload",
    response_model=ResumeResponse,
    status_code=200,
    description="Upload and parse a resume file (PDF, DOC, or DOCX)"
)
async def upload_resume(
    resume: UploadFile = File(
        ...,
        description="Resume file (PDF, DOC, or DOCX)",
        media_type="multipart/form-data"
    )
):
    """
    Upload and parse resume file
    
    - **file**: Resume file in PDF, DOC, or DOCX format
    - Form field name must be 'file'
    """
    try:
        # Check if file was uploaded
        if not resume:
            raise HTTPException(
                status_code=400,
                detail="No file uploaded. Please use 'file' as the form field name."
            )

        # Validate file extension
        file_ext = os.path.splitext(resume.filename.lower())[1]
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Check file size (5MB limit)
        content = await resume.read()
        if len(content) > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 5MB"
            )

        # Reset file pointer
        await resume.seek(0)
        
        logger.info(f"Processing file: {resume.filename} ({file_ext})")

        # Initialize resume service
        resume_service = ResumeService()

        try:
            # Parse resume
            parsed_data = resume_service.parse_resume(resume.file)
            
            # Determine domain based on skills
            domain = resume_service.determine_domain(parsed_data['skills'])
            
            # Determine skill level based on experience and skills
            skill_level = resume_service.determine_skill_level(
                parsed_data['experience'],
                parsed_data['skills']
            )

            # Create and validate response
            response = ResumeResponse(
                skills=parsed_data['skills'],
                experience=parsed_data['experience'],
                education=parsed_data['education'],
                domain=domain,
                skill_level=skill_level
            )

            logger.info(f"Successfully processed resume. Domain: {domain}, Level: {skill_level}")
            return response

        except Exception as e:
            logger.error(f"Error processing resume content: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error processing resume: {str(e)}"
            )

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        # Clean up
        await resume.close()

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
            