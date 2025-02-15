# -*- coding: utf-8 -*-
import re
from typing import BinaryIO, Dict, List
import PyPDF2
from docx import Document
import magic
import io

class ResumeService:
    def __init__(self):
        self.nlp = None
        self.web_dev_keywords = {
            'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node', 'frontend', 'backend'
        }
        self.ai_ml_keywords = {
            'machine learning', 'ai', 'deep learning', 'neural networks', 'python', 'tensorflow', 'pytorch'
        }
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Warning: spaCy not available, using basic parsing: {str(e)}")
        self.allowed_mime_types = {
            'application/pdf': '.pdf',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
        }

    def parse_resume(self, file: BinaryIO) -> Dict[str, List[str]]:
        """Parse resume file and extract relevant information"""
        try:
            # Read file content and detect type
            content = file.read()
            mime_type = magic.from_buffer(content, mime=True)
            
            if mime_type not in self.allowed_mime_types:
                raise ValueError(f"Unsupported file type: {mime_type}")
            
            # Extract text based on file type
            if mime_type == 'application/pdf':
                text = self._extract_text_from_pdf(content)
            elif mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                text = self._extract_text_from_docx(content)
            else:
                raise ValueError("Unsupported file type")
            
            # Split text into sections
            sections = self._split_into_sections(text)
            
            return {
                'skills': sections.get('SKILLS', []),
                'experience': sections.get('EXPERIENCE', []),
                'education': sections.get('EDUCATION', [])
            }
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")

    def _extract_text_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            pdf_file = io.BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _extract_text_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc_file = io.BytesIO(content)
            doc = Document(doc_file)
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
                
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")

    def _split_into_sections(self, text: str) -> Dict[str, List[str]]:
        """Split text into sections"""
        sections = {}
        current_section = None
        current_content = []
        
        # Split text into lines and process each line
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a section header
            upper_line = line.upper()
            if any(section in upper_line for section in ['SKILLS', 'EXPERIENCE', 'EDUCATION']):
                # Save previous section if exists
                if current_section and current_content:
                    sections[current_section] = current_content
                
                # Start new section
                current_section = next(s for s in ['SKILLS', 'EXPERIENCE', 'EDUCATION'] if s in upper_line)
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = current_content
        
        # Process skills section (comma-separated)
        if 'SKILLS' in sections:
            skills_text = ' '.join(sections['SKILLS'])
            sections['SKILLS'] = [s.strip() for s in skills_text.split(',') if s.strip()]
        
        # Limit section sizes
        return {
            'SKILLS': sections.get('SKILLS', [])[:10],
            'EXPERIENCE': sections.get('EXPERIENCE', [])[:5],
            'EDUCATION': sections.get('EDUCATION', [])[:3]
        }

    def _get_section(self, text: str, section_name: str) -> str:
        """Extract section from text"""
        pattern = f"{section_name}.*?(?=\\n\\n|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            section = match.group(0)
            section = re.sub(f"{section_name}.*?\\n", '', section, flags=re.IGNORECASE)
            return section.strip()
        return ""

    def _basic_extract_skills(self, text):
        """Basic skill extraction without spaCy"""
        common_skills = ['python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular', 'node']
        found_skills = []
        for skill in common_skills:
            if re.search(r'\b' + skill + r'\b', text.lower()):
                found_skills.append(skill)
        return found_skills

    def _basic_extract_experience(self, text):
        """Basic experience extraction without spaCy"""
        experiences = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['work', 'job', 'position', 'experience']):
                experiences.append(line.strip())
        return experiences[:5]

    def _basic_extract_education(self, text):
        """Basic education extraction without spaCy"""
        education = []
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['degree', 'university', 'college', 'school']):
                education.append(line.strip())
        return education[:3]

    def determine_domain(self, skills: List[str]) -> str:
        """Determine if candidate is web dev or AI/ML"""
        web_dev_count = sum(1 for skill in skills if skill.lower() in self.web_dev_keywords)
        ai_ml_count = sum(1 for skill in skills if skill.lower() in self.ai_ml_keywords)
        
        return 'web_dev' if web_dev_count > ai_ml_count else 'ai_ml'

    def determine_skill_level(self, experience: List[str], skills: List[str]) -> str:
        """Determine candidate's skill level"""
        # Count years of experience
        years = 0
        for exp in experience:
            if 'year' in exp.lower():
                try:
                    years = max(years, int(exp.split()[0]))
                except:
                    continue

        # Basic skill level determination
        if years > 5 or len(skills) > 10:
            return 'expert'
        elif years > 2 or len(skills) > 5:
            return 'intermediate'
        else:
            return 'beginner' 