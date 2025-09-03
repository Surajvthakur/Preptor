# assessment_engine.py
import random
import json
from typing import Dict, List, Any
from textblob import TextBlob

class AssessmentEngine:
    def __init__(self):
        self.aptitude_questions = self._load_aptitude_questions()
        self.technical_questions = self._load_technical_questions()
        self.behavioral_questions = self._load_behavioral_questions()
    
    def _load_aptitude_questions(self) -> List[Dict[str, Any]]:
        """Load aptitude questions database"""
        return [
            {
                "id": 1,
                "question": "If a train travels 120 km in 2 hours, what is its speed in m/s?",
                "options": ["16.67 m/s", "33.33 m/s", "60 m/s", "120 m/s"],
                "correct": 0,
                "type": "quantitative",
                "difficulty": "medium"
            },
            {
                "id": 2,
                "question": "Complete the series: 2, 6, 18, 54, ?",
                "options": ["108", "162", "216", "324"],
                "correct": 1,
                "type": "logical",
                "difficulty": "medium"
            },
            {
                "id": 3,
                "question": "Choose the word most similar to 'Euphoric':",
                "options": ["Sad", "Elated", "Angry", "Confused"],
                "correct": 1,
                "type": "verbal",
                "difficulty": "easy"
            },
            # Add more questions...
        ]
    
    def _load_technical_questions(self) -> List[Dict[str, Any]]:
        """Load technical questions database"""
        return [
            {
                "id": 1,
                "question": "What is the time complexity of binary search?",
                "options": ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
                "correct": 1,
                "topic": "DSA",
                "difficulty": "easy"
            },
            {
                "id": 2,
                "question": "Which SQL command is used to retrieve data?",
                "options": ["INSERT", "UPDATE", "SELECT", "DELETE"],
                "correct": 2,
                "topic": "DBMS",
                "difficulty": "easy"
            },
            {
                "id": 3,
                "question": "What is a deadlock in operating systems?",
                "options": [
                    "A process that never terminates",
                    "Two or more processes waiting indefinitely for each other",
                    "A corrupted file system",
                    "Memory overflow condition"
                ],
                "correct": 1,
                "topic": "OS",
                "difficulty": "medium"
            },
            # Add more questions...
        ]
    
    def _load_behavioral_questions(self) -> List[str]:
        """Load behavioral interview questions"""
        return [
            "Tell me about yourself",
            "What are your strengths and weaknesses?",
            "Describe a challenging project you worked on",
            "How do you handle stress and pressure?",
            "Where do you see yourself in 5 years?",
            "Why should we hire you?",
            "Describe a time when you worked in a team",
            "How do you stay updated with technology trends?"
        ]
    
    def generate_aptitude_test(self, num_questions: int = 20) -> List[Dict[str, Any]]:
        """Generate randomized aptitude test"""
        return random.sample(self.aptitude_questions, min(num_questions, len(self.aptitude_questions)))
    
    def generate_technical_test(self, branch: str, num_questions: int = 15) -> List[Dict[str, Any]]:
        """Generate technical test based on branch"""
        # Filter questions based on branch relevance
        relevant_questions = self.technical_questions
        if branch.lower() in ['cse', 'it']:
            relevant_questions = [q for q in self.technical_questions if q['topic'] in ['DSA', 'DBMS', 'OS']]
        
        return random.sample(relevant_questions, min(num_questions, len(relevant_questions)))
    
    def evaluate_aptitude_test(self, answers: List[int], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate aptitude test results"""
        correct_answers = 0
        topic_scores = {"quantitative": 0, "logical": 0, "verbal": 0}
        topic_counts = {"quantitative": 0, "logical": 0, "verbal": 0}
        
        for i, answer in enumerate(answers):
            question = questions[i]
            topic = question["type"]
            topic_counts[topic] += 1
            
            if answer == question["correct"]:
                correct_answers += 1
                topic_scores[topic] += 1
        
        # Calculate percentage scores
        overall_score = (correct_answers / len(questions)) * 100
        
        for topic in topic_scores:
            if topic_counts[topic] > 0:
                topic_scores[topic] = (topic_scores[topic] / topic_counts[topic]) * 100
        
        return {
            "overall_score": overall_score,
            "topic_scores": topic_scores,
            "correct_answers": correct_answers,
            "total_questions": len(questions),
            "weak_areas": [topic for topic, score in topic_scores.items() if score < 60]
        }
    
    def evaluate_technical_test(self, answers: List[int], questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate technical test results"""
        correct_answers = 0
        topic_scores = {}
        topic_counts = {}
        
        for i, answer in enumerate(answers):
            question = questions[i]
            topic = question["topic"]
            
            if topic not in topic_scores:
                topic_scores[topic] = 0
                topic_counts[topic] = 0
            
            topic_counts[topic] += 1
            
            if answer == question["correct"]:
                correct_answers += 1
                topic_scores[topic] += 1
        
        # Calculate percentage scores
        overall_score = (correct_answers / len(questions)) * 100
        
        for topic in topic_scores:
            if topic_counts[topic] > 0:
                topic_scores[topic] = (topic_scores[topic] / topic_counts[topic]) * 100
        
        return {
            "overall_score": overall_score,
            "topic_scores": topic_scores,
            "correct_answers": correct_answers,
            "total_questions": len(questions),
            "weak_areas": [topic for topic, score in topic_scores.items() if score < 60]
        }
    
    def analyze_communication(self, text_response: str) -> Dict[str, Any]:
        """Analyze communication skills from text response"""
        blob = TextBlob(text_response)
        
        # Basic metrics
        word_count = len(text_response.split())
        sentence_count = len(blob.sentences)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Sentiment and confidence analysis
        sentiment = blob.sentiment
        confidence_score = min(100, max(0, (sentiment.polarity + 1) * 50))
        
        # Grammar and vocabulary assessment (simplified)
        grammar_score = max(0, 100 - (text_response.count('.') * 5))  # Simplified
        vocabulary_score = min(100, len(set(text_response.lower().split())) * 2)
        
        overall_score = (confidence_score + grammar_score + vocabulary_score) / 3
        
        return {
            "overall_score": overall_score,
            "confidence_score": confidence_score,
            "grammar_score": grammar_score,
            "vocabulary_score": vocabulary_score,
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "sentiment": sentiment.polarity,
            "areas_for_improvement": self._get_communication_improvements(overall_score)
        }
    
    def _get_communication_improvements(self, score: float) -> List[str]:
        """Get communication improvement suggestions"""
        improvements = []
        
        if score < 50:
            improvements.extend([
                "Practice speaking clearly and confidently",
                "Expand vocabulary through reading",
                "Work on grammar and sentence structure"
            ])
        elif score < 70:
            improvements.extend([
                "Practice articulating complex ideas simply",
                "Work on professional communication tone"
            ])
        else:
            improvements.append("Continue practicing to maintain excellent communication")
        
        return improvements