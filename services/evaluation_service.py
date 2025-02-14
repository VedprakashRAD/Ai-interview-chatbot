# -*- coding: utf-8 -*-
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EvaluationService:
    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load SentenceTransformer model: {str(e)}")
            self.model = None
    
    def evaluate_answers(self, answers):
        """Evaluate interview answers"""
        if not answers:
            return self._empty_evaluation()
            
        if not self.model:
            return self._fallback_evaluation(answers)
            
        try:
            total_score = 0
            strengths = []
            weaknesses = []
            
            for answer in answers:
                score = self._evaluate_single_answer(
                    answer['question'],
                    answer['answer'],
                    answer.get('expected_keywords', [])
                )
                total_score += score
                
                if score >= 0.7:
                    strengths.append(f"Strong understanding of {answer['question']}")
                elif score <= 0.4:
                    weaknesses.append(f"Need improvement in {answer['question']}")
            
            avg_score = total_score / len(answers)
            
            return {
                'score': float(avg_score),
                'feedback': self._generate_feedback(avg_score),
                'strengths': strengths,
                'weaknesses': weaknesses,
                'recommendations': self._generate_recommendations(weaknesses)
            }
        except Exception as e:
            print(f"Error in evaluate_answers: {str(e)}")
            return self._fallback_evaluation(answers)
    
    def _empty_evaluation(self):
        return {
            'score': 0.0,
            'feedback': "No answers provided for evaluation.",
            'strengths': [],
            'weaknesses': [],
            'recommendations': ["Please provide answers for evaluation."]
        }
    
    def _fallback_evaluation(self, answers):
        return {
            'score': 0.5,
            'feedback': "Basic evaluation performed due to technical limitations.",
            'strengths': ["Answer provided"],
            'weaknesses': ["Detailed evaluation not available"],
            'recommendations': ["Please try again later for detailed evaluation."]
        }
    
    def _evaluate_single_answer(self, question, answer, expected_keywords):
        """Evaluate a single answer using semantic similarity"""
        if not answer:
            return 0.0
        
        # Encode the answer and expected keywords
        answer_embedding = self.model.encode([answer])[0]
        keyword_embeddings = self.model.encode(expected_keywords)
        
        # Calculate similarity with keywords
        similarities = cosine_similarity([answer_embedding], keyword_embeddings)[0]
        return float(np.mean(similarities))
    
    def _generate_feedback(self, score):
        if score >= 0.8:
            return "Excellent performance! You demonstrated strong knowledge across most topics."
        elif score >= 0.6:
            return "Good performance. There's room for improvement in some areas."
        else:
            return "More preparation needed. Focus on strengthening core concepts."
    
    def _generate_recommendations(self, weaknesses):
        recommendations = []
        for weakness in weaknesses:
            recommendations.append(f"Study more about {weakness.split('in ')[-1]}")
        return recommendations 