# Create setup.ps1 file
@'
# Setup script for AI Interview Chatbot

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Green
$dirs = @(
    "api",
    "api/routes",
    "api/models",
    "services",
    "data/ai_ml",
    "data/web_dev",
    "uploads"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir
}

# Create __init__.py files
Write-Host "Creating __init__.py files..." -ForegroundColor Green
$init_files = @(
    "api/__init__.py",
    "api/routes/__init__.py",
    "api/models/__init__.py",
    "services/__init__.py"
)

foreach ($file in $init_files) {
    Set-Content -Path $file -Value "# -*- coding: utf-8 -*-`n" -Encoding UTF8
}

# Create route files
Write-Host "Creating route files..." -ForegroundColor Green

# resume_routes.py
$resume_content = @'
# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from flask import request
from services.resume_service import ResumeService
from werkzeug.datastructures import FileStorage

resume_ns = Namespace("resume", description="Resume operations")

resume_model = resume_ns.model("Resume", {
    "skills": fields.List(fields.String),
    "experience": fields.List(fields.String),
    "education": fields.List(fields.String)
})

upload_parser = resume_ns.parser()
upload_parser.add_argument("file", 
                         type=FileStorage, 
                         location="files", 
                         required=True)

@resume_ns.route("/upload")
class ResumeUpload(Resource):
    @resume_ns.expect(upload_parser)
    @resume_ns.response(201, "Success", resume_model)
    def post(self):
        args = upload_parser.parse_args()
        resume_file = args["file"]
        
        try:
            resume_service = ResumeService()
            parsed_data = resume_service.parse_resume(resume_file)
            return parsed_data, 201
        except Exception as e:
            resume_ns.abort(400, str(e))
'@
Set-Content -Path "api/routes/resume_routes.py" -Value $resume_content -Encoding UTF8

# question_routes.py
$question_content = @'
# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from services.question_service import QuestionService

question_ns = Namespace("questions", description="Question operations")

question_model = question_ns.model("Question", {
    "id": fields.String,
    "category": fields.String,
    "difficulty": fields.String,
    "question": fields.String,
    "expected_keywords": fields.List(fields.String)
})

@question_ns.route("/<string:category>")
class Questions(Resource):
    @question_ns.marshal_list_with(question_model)
    def get(self, category):
        try:
            question_service = QuestionService()
            questions = question_service.get_questions_by_category(category)
            return questions
        except Exception as e:
            question_ns.abort(400, str(e))
'@
Set-Content -Path "api/routes/question_routes.py" -Value $question_content -Encoding UTF8

# evaluation_routes.py
$evaluation_content = @'
# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from services.evaluation_service import EvaluationService

evaluation_ns = Namespace("evaluation", description="Evaluation operations")

evaluation_model = evaluation_ns.model("Evaluation", {
    "score": fields.Float,
    "feedback": fields.String,
    "strengths": fields.List(fields.String),
    "weaknesses": fields.List(fields.String),
    "recommendations": fields.List(fields.String)
})

@evaluation_ns.route("/evaluate")
class Evaluate(Resource):
    @evaluation_ns.expect(evaluation_ns.model("Answers", {
        "answers": fields.List(fields.Raw)
    }))
    @evaluation_ns.marshal_with(evaluation_model)
    def post(self):
        try:
            data = evaluation_ns.payload
            evaluation_service = EvaluationService()
            evaluation = evaluation_service.evaluate_answers(data["answers"])
            return evaluation
        except Exception as e:
            evaluation_ns.abort(400, str(e))
'@
Set-Content -Path "api/routes/evaluation_routes.py" -Value $evaluation_content -Encoding UTF8

# Create/activate virtual environment and install packages
Write-Host "Setting up Python environment..." -ForegroundColor Green
python -m venv venv
.\venv\Scripts\Activate
pip install flask==3.0.2
pip install flask-restx==1.3.0
pip install spacy==3.7.4
pip install sentence-transformers==2.5.1
pip install scikit-learn==1.4.1
pip install flask-cors==4.0.0
pip install numpy==1.26.4

# Install spaCy model
python -m spacy download en_core_web_sm
