# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

class QuestionService:
    def __init__(self):
        self.questions_cache = {}
        self.load_questions()
    
    def load_questions(self):
        """Load questions from JSON files"""
        categories = ['ai_ml', 'web_dev']
        for category in categories:
            path = Path(f'data/{category}')
            if not path.exists():
                print(f"Warning: Directory {path} does not exist")
                continue
                
            try:
                for file_path in path.glob('*.json'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            category_name = file_path.stem.split('_')[0]  # Get category from filename
                            self.questions_cache[category_name] = data['questions']
                    except Exception as e:
                        print(f"Error loading {file_path}: {str(e)}")
            except Exception as e:
                print(f"Error accessing directory {path}: {str(e)}")
    
    def get_questions_by_category(self, category):
        """Get questions for a specific category"""
        if category not in self.questions_cache:
            return []  # Return empty list instead of raising exception
        return self.questions_cache[category]
    
    def get_next_question(self, previous_question_id, answer):
        """Get next question based on previous answer"""
        if not previous_question_id:
            # If no previous question, return first question from any category
            for questions in self.questions_cache.values():
                if questions:
                    return questions[0]
            return None
            
        # Find next question in sequence
        for questions in self.questions_cache.values():
            for i, q in enumerate(questions):
                if q['id'] == previous_question_id and i + 1 < len(questions):
                    return questions[i + 1]
        return None 