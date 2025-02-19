# -*- coding: utf-8 -*-
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional
import logging
import os
from api.models.resume import ResumeResponse
from services.resume_service import ResumeService
from models.candidate import Candidate, Domain
from services.photo_service import PhotoService
from services.id_service import IDService

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

resume_service = ResumeService()
photo_service = PhotoService()
id_service = IDService()

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

@router.post("/register")
async def register_candidate(
    name: str = Form(...),
    father_name: str = Form(...),
    email: str = Form(...),
    domain: Domain = Form(...),
    resume: UploadFile = File(...),
    photo: UploadFile = File(...)
):
    try:
        # Process resume
        resume_content = await resume.read()
        resume_path = resume_service.save_resume(resume_content, resume.filename)
        parsed_resume = resume_service.parse_resume(resume_path)

        # Process photo
        photo_content = await photo.read()
        photo_path = photo_service.save_photo(photo_content)

        # Generate IDs
        candidate_id = id_service.generate_candidate_id()
        test_id = id_service.generate_test_id()

        # Create candidate
        candidate = Candidate(
            candidate_id=candidate_id,
            test_id=test_id,
            name=name,
            father_name=father_name,
            email=email,
            domain=domain,
            resume_path=resume_path,
            photo_path=photo_path,
            parsed_resume_data=parsed_resume
        )

        # Here you would typically save the candidate to a database
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Registration successful",
                "candidate_id": candidate_id,
                "test_id": test_id,
                "parsed_resume": parsed_resume
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            