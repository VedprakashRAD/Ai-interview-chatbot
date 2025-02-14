# -*- coding: utf-8 -*-
from flask import Flask, redirect
from flask_restx import Api
from flask_cors import CORS
from api.routes.resume_routes import resume_ns
from api.routes.question_routes import question_ns
from api.routes.evaluation_routes import evaluation_ns
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    
    # Create API with Swagger documentation
    api = Api(
        app,
        version='1.0',
        title='AI Interview Chatbot API',
        description='API for AI-powered interview chatbot',
        doc='/docs'
    )
    
    # Add namespaces
    api.add_namespace(resume_ns, path='/api/resume')
    api.add_namespace(question_ns, path='/api/questions')
    api.add_namespace(evaluation_ns, path='/api/evaluation')
    
    # Redirect root to Swagger docs
    @app.route('/')
    def index():
        return redirect('/docs')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 