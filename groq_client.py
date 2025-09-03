# groq_client.py
from groq import Groq
from typing import Dict, Any, List
import json
import config

class GroqClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = config.config.GROQ_MODEL
    
    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """Generate response using Groq API"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume and extract key information"""
        prompt = f"""
        Analyze the following resume and extract:
        1. Technical skills mentioned
        2. Projects and their descriptions
        3. Academic achievements
        4. Work experience
        5. Areas for improvement
        6. ATS score (0-100) based on keyword relevance and formatting
        
        Resume text:
        {resume_text}
        
        Return response in JSON format with keys: skills, projects, achievements, experience, improvements, ats_score
        """
        
        system_prompt = "You are an expert resume analyzer. Provide detailed analysis in valid JSON format."
        response = self.generate_response(prompt, system_prompt)
        
        try:
            return json.loads(response)
        except:
            return {
                "skills": [],
                "projects": [],
                "achievements": [],
                "experience": [],
                "improvements": ["Resume analysis failed"],
                "ats_score": 50
            }
    
    def generate_study_plan(self, skill_profile: Dict[str, Any], 
                          target_company: str = "") -> Dict[str, Any]:
        """Generate personalized study plan"""
        prompt = f"""
        Create a personalized study plan for a student with the following profile:
        
        Current Skills: {skill_profile}
        Target Company: {target_company}
        
        Generate a 4-week study plan with:
        1. Daily topics to cover
        2. Practice questions per day
        3. Resources needed
        4. Milestones and checkpoints
        5. Company-specific preparation tips
        
        Return in JSON format with keys: week1, week2, week3, week4, daily_goals, milestones
        """
        
        system_prompt = "You are an expert placement preparation mentor. Create structured, actionable study plans."
        response = self.generate_response(prompt, system_prompt)
        
        try:
            return json.loads(response)
        except:
            return {"error": "Failed to generate study plan"}