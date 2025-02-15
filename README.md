# AI Interview Chatbot

An intelligent interview system that analyzes resumes and conducts domain-specific technical interviews.

## Features

- **Resume Analysis**
  - PDF, DOC, DOCX support
  - Skills extraction
  - Experience analysis
  - Education details parsing
  - Domain detection (Web Development/AI-ML)
  - Skill level assessment

- **Dynamic Question Generation**
  - Domain-specific questions (Web Dev/AI-ML)
  - 15 questions per interview
    - 5 Easy questions
    - 5 Medium questions
    - 5 Hard questions
  - Adaptive difficulty based on skill level

- **Evaluation System**
  - Real-time answer evaluation
  - Score calculation (out of 100)
  - Detailed feedback
  - Strengths and weaknesses analysis
  - Improvement recommendations

## Project Structure

interview_chatbot/
├── api/
│ ├── init.py
│ ├── routes/
│ │ ├── init.py
│ │ ├── resume_routes.py      # Resume upload & parsing
│ │ ├── question_routes.py    # Question generation
│ │ └── evaluation_routes.py  # Answer evaluation
│ └── models/
│ ├── init.py
│ ├── resume.py              # Resume data models
│ ├── question.py            # Question models
│ └── evaluation.py          # Evaluation models
├── data/
│ ├── ai_ml/                 # AI/ML questions
│ │ ├── ai_questions.json
│ │ ├── ml_questions.json
│ │ └── advanced_questions.json
│ └── web_dev/               # Web Dev questions
│ ├── html_questions.json
│ ├── css_questions.json
│ └── javascript_questions.json
├── services/
│ ├── init.py
│ ├── resume_service.py      # Resume processing logic
│ ├── question_service.py    # Question management
│ └── evaluation_service.py  # Evaluation logic
├── config.py                # Configuration settings
├── requirements.txt         # Project dependencies
└── app.py                   # Application entry point

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VedprakashRAD/Ai-interview-chatbot.git
cd Ai-interview-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Configuration

Update `config.py` with your settings:
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
```

## Running the Application

1. Start the server:
```bash
python app.py
```

2. Access the API at `http://127.0.0.1:8001`

## API Endpoints

### 1. Resume Upload
```http
POST /api/resume/upload
Content-Type: multipart/form-data

file: resume.pdf/doc/docx
```

Response:
```json
{
    "skills": ["Python", "FastAPI", "Machine Learning"],
    "experience": ["Senior Developer", "Tech Lead"],
    "education": ["Master in Computer Science"],
    "domain": "ai_ml",
    "skill_level": "intermediate"
}
```

### 2. Get Questions
```http
GET /api/questions/{domain}/{skill_level}
```

Response:
```json
[
    {
        "id": "q1",
        "category": "ai_ml",
        "difficulty": "intermediate",
        "question": "Explain neural networks",
        "expected_keywords": ["layers", "neurons", "activation"]
    }
]
```

### 3. Submit Evaluation
```http
POST /api/evaluation/evaluate
Content-Type: application/json

{
    "answers": [
        {
            "question_id": "q1",
            "answer": "Detailed answer here"
        }
    ]
}
```

Response:
```json
{
    "score": 85,
    "feedback": "Excellent understanding of concepts",
    "strengths": ["Technical knowledge", "Clear explanation"],
    "weaknesses": ["Could add more examples"],
    "recommendations": ["Practice more coding questions"]
}
```

## Directory Details

### API Structure
- `api/routes/`: Contains all API endpoint definitions
- `api/models/`: Data models and schemas
- `services/`: Business logic implementation
- `data/`: Question banks for different domains

### Question Categories
- **AI/ML**:
  - AI fundamentals
  - Machine Learning concepts
  - Advanced topics
- **Web Development**:
  - HTML/CSS
  - JavaScript
  - Frontend/Backend concepts

## Development

1. Install development dependencies:
```bash
pip install pytest black flake8
```

2. Run tests:
```bash
python -m pytest
```

3. Format code:
```bash
black .
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

Vedprakash - [@VedprakashRAD](https://github.com/VedprakashRAD)

Project Link: [https://github.com/VedprakashRAD/Ai-interview-chatbot](https://github.com/VedprakashRAD/Ai-interview-chatbot)
```

Key updates made:
1. Updated project structure to match new format
2. Added detailed API response examples
3. Included configuration section
4. Added directory details section
5. Updated installation instructions
6. Added development section
7. Improved formatting throughout
8. Added question categories section
9. Included more detailed API documentation
10. Updated all code examples to match current implementation

Let me know if you need any modifications!
