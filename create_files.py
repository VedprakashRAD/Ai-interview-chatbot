import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

# Create directories
os.makedirs('api/routes', exist_ok=True)

# __init__.py
init_content = '''# -*- coding: utf-8 -*-
'''

# resume_routes.py
resume_content = '''# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from flask import request
from services.resume_service import ResumeService
from werkzeug.datastructures import FileStorage

resume_ns = Namespace('resume', description='Resume operations')

resume_model = resume_ns.model('Resume', {
    'skills': fields.List(fields.String),
    'experience': fields.List(fields.String),
    'education': fields.List(fields.String)
})

upload_parser = resume_ns.parser()
upload_parser.add_argument('file', 
                         type=FileStorage, 
                         location='files', 
                         required=True)

@resume_ns.route('/upload')
class ResumeUpload(Resource):
    @resume_ns.expect(upload_parser)
    @resume_ns.response(201, 'Success', resume_model)
    def post(self):
        args = upload_parser.parse_args()
        resume_file = args['file']
        
        try:
            resume_service = ResumeService()
            parsed_data = resume_service.parse_resume(resume_file)
            return parsed_data, 201
        except Exception as e:
            resume_ns.abort(400, str(e))
'''

# evaluation_routes.py
evaluation_content = '''# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from services.evaluation_service import EvaluationService

evaluation_ns = Namespace('evaluation', description='Evaluation operations')

evaluation_model = evaluation_ns.model('Evaluation', {
    'score': fields.Float,
    'feedback': fields.String,
    'strengths': fields.List(fields.String),
    'weaknesses': fields.List(fields.String),
    'recommendations': fields.List(fields.String)
})

@evaluation_ns.route('/evaluate')
class Evaluate(Resource):
    @evaluation_ns.expect(evaluation_ns.model('Answers', {
        'answers': fields.List(fields.Raw)
    }))
    @evaluation_ns.marshal_with(evaluation_model)
    def post(self):
        try:
            data = evaluation_ns.payload
            evaluation_service = EvaluationService()
            evaluation = evaluation_service.evaluate_answers(data['answers'])
            return evaluation
        except Exception as e:
            evaluation_ns.abort(400, str(e))
'''

# question_routes.py
question_content = '''# -*- coding: utf-8 -*-
from flask_restx import Namespace, Resource, fields
from services.question_service import QuestionService

question_ns = Namespace('questions', description='Question operations')

question_model = question_ns.model('Question', {
    'id': fields.String,
    'category': fields.String,
    'difficulty': fields.String,
    'question': fields.String,
    'expected_keywords': fields.List(fields.String)
})

@question_ns.route('/<string:category>')
class Questions(Resource):
    @question_ns.marshal_list_with(question_model)
    def get(self, category):
        try:
            question_service = QuestionService()
            questions = question_service.get_questions_by_category(category)
            return questions
        except Exception as e:
            question_ns.abort(400, str(e))

@question_ns.route('/next')
class NextQuestion(Resource):
    @question_ns.expect(question_ns.model('PreviousAnswer', {
        'previous_question_id': fields.String,
        'answer': fields.String
    }))
    @question_ns.marshal_with(question_model)
    def post(self):
        try:
            data = question_ns.payload
            question_service = QuestionService()
            next_question = question_service.get_next_question(
                data['previous_question_id'],
                data['answer']
            )
            return next_question
        except Exception as e:
            question_ns.abort(400, str(e))
'''

# Write files
write_file('api/routes/__init__.py', init_content)
write_file('api/routes/resume_routes.py', resume_content)
write_file('api/routes/evaluation_routes.py', evaluation_content)
write_file('api/routes/question_routes.py', question_content)

print('Files created successfully!')
