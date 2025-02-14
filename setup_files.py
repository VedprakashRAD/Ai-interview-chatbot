import os

def create_file(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

# Create directories
os.makedirs('api/routes', exist_ok=True)

# Create __init__.py
init_content = """# -*- coding: utf-8 -*-
"""

# Create resume_routes.py
resume_content = """# -*- coding: utf-8 -*-
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
"""

# Create files
create_file('api/routes/__init__.py', init_content)
create_file('api/routes/resume_routes.py', resume_content)

print('Files created successfully!')
