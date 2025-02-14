import requests
from pathlib import Path

def test_resume_upload():
    url = 'http://127.0.0.1:8001/api/resume/upload'
    
    # Create sample resume
    resume_content = """SKILLS
Python, FastAPI, Machine Learning

EXPERIENCE
Senior Software Developer
- AI Development
- API Design

EDUCATION
Master in Computer Science"""

    # Save resume to file
    resume_file = Path('test_resume.txt')
    resume_file.write_text(resume_content)
    
    try:
        # Upload file
        with open(resume_file, 'rb') as f:
            # Important: Make sure the file field name matches exactly
            files = {
                'file': ('resume.txt', f, 'text/plain')
            }
            # Add proper headers
            headers = {
                'accept': 'application/json',
                'Content-Type': 'multipart/form-data'
            }
            
            # Make the request
            response = requests.post(
                url,
                files=files,
                headers=headers,
                timeout=30
            )
        
        # Print results
        print(f"Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Raw Response: {response.text}")
        
        if response.ok:
            try:
                data = response.json()
                print("\nParsed Resume:")
                print("\nSkills:")
                for skill in data['skills']:
                    print(f"- {skill}")
                print("\nExperience:")
                for exp in data['experience']:
                    print(f"- {exp}")
                print("\nEducation:")
                for edu in data['education']:
                    print(f"- {edu}")
            except Exception as e:
                print(f"Error parsing response: {e}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if resume_file.exists():
            resume_file.unlink()

if __name__ == "__main__":
    test_resume_upload() 