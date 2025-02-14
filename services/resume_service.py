# -*- coding: utf-8 -*-
import re
from typing import BinaryIO, Dict, List

class ResumeService:
    def __init__(self):
        self.nlp = None
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except Exception as e:
            print(f"Warning: spaCy not available, using basic parsing: {str(e)}")

    def parse_resume(self, file: BinaryIO) -> Dict[str, List[str]]:
        """Parse resume file and extract relevant information"""
        try:
            # Read file content
            text = file.read().decode('utf-8')
            
            # Split text into sections
            sections = self._split_into_sections(text)
            
            return {
                'skills': sections.get('SKILLS', []),
                'experience': sections.get('EXPERIENCE', []),
                'education': sections.get('EDUCATION', [])
            }
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")

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