# job_matcher.py
import requests
from typing import List, Dict, Any
import json
from groq_client import GroqClient
from config import config

class JobMatcher:
    def __init__(self):
        self.groq_client = GroqClient(config.GROQ_API_KEY)
    
    def get_mock_job_listings(self) -> List[Dict[str, Any]]:
        """Get mock job listings (replace with actual API integration)"""
        return [
            {
                "title": "Software Developer Trainee",
                "company": "TCS",
                "location": "Pune, India",
                "requirements": ["Programming in Java/C++", "Basic DSA knowledge", "Good communication"],
                "description": "Entry-level position for fresh graduates in software development",
                "url": "https://careers.tcs.com/entry-level",
                "posted_date": "2024-01-15"
            },
            {
                "title": "Systems Engineer",
                "company": "Infosys",
                "location": "Bangalore, India", 
                "requirements": ["Programming skills", "Database knowledge", "Problem-solving"],
                "description": "Graduate trainee program for systems engineering",
                "url": "https://careers.infosys.com/graduate-program",
                "posted_date": "2024-01-14"
            },
            {
                "title": "Software Development Engineer I",
                "company": "Amazon",
                "location": "Hyderabad, India",
                "requirements": ["Strong DSA skills", "System design basics", "AWS knowledge"],
                "description": "Entry-level SDE position with growth opportunities",
                "url": "https://amazon.jobs/en/jobs/sde1",
                "posted_date": "2024-01-13"
            },
            {
                "title": "Associate Software Engineer",
                "company": "Microsoft",
                "location": "Noida, India",
                "requirements": ["Programming proficiency", "Algorithm design", "Team collaboration"],
                "description": "Graduate program for software engineering",
                "url": "https://careers.microsoft.com/associate-engineer",
                "posted_date": "2024-01-12"
            }
        ]
    
    def calculate_job_fit(self, user_skills: Dict[str, float], job_requirements: List[str]) -> float:
        """Calculate job fit score based on user skills and requirements"""
        if not job_requirements:
            return 50.0
        
        # Simple matching algorithm (can be enhanced with NLP)
        skill_keywords = {
            "programming": ["programming", "coding", "java", "python", "c++"],
            "dsa": ["dsa", "algorithms", "data structures", "problem-solving"],
            "database": ["database", "sql", "dbms", "mysql"],
            "communication": ["communication", "team", "collaboration"]
        }
        
        matched_skills = 0
        total_requirements = len(job_requirements)
        
        for requirement in job_requirements:
            req_lower = requirement.lower()
            for skill_area, keywords in skill_keywords.items():
                if any(keyword in req_lower for keyword in keywords):
                    # Weight by user's skill level in that area
                    skill_score = user_skills.get(skill_area, 0) / 100
                    matched_skills += skill_score
                    break
        
        fit_score = (matched_skills / total_requirements) * 100
        return min(100, max(0, fit_score))
    
    def match_jobs(self, user_profile: Dict[str, Any], 
                   skill_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Match jobs based on user profile and skills"""
        job_listings = self.get_mock_job_listings()
        matched_jobs = []
        
        # Convert assessment scores to skill areas
        user_skills = {
            "programming": skill_scores.get("technical", 0),
            "dsa": skill_scores.get("technical", 0),
            "database": skill_scores.get("technical", 0) * 0.8,
            "communication": skill_scores.get("communication", 0)
        }
        
        for job in job_listings:
            fit_score = self.calculate_job_fit(user_skills, job["requirements"])
            
            # Categorize fit level
            if fit_score >= 80:
                fit_level = "High Fit"
            elif fit_score >= 60:
                fit_level = "Medium Fit"
            else:
                fit_level = "Low Fit"
            
            matched_job = {
                **job,
                "fit_score": round(fit_score, 1),
                "fit_level": fit_level,
                "matching_skills": self._get_matching_skills(user_skills, job["requirements"]),
                "skill_gaps": self._get_skill_gaps(user_skills, job["requirements"])
            }
            
            matched_jobs.append(matched_job)
        
        # Sort by fit score
        matched_jobs.sort(key=lambda x: x["fit_score"], reverse=True)
        return matched_jobs
    
    def _get_matching_skills(self, user_skills: Dict[str, float], 
                           requirements: List[str]) -> List[str]:
        """Get skills that match job requirements"""
        matching = []
        for req in requirements:
            req_lower = req.lower()
            if "programming" in req_lower and user_skills.get("programming", 0) > 60:
                matching.append("Programming Skills")
            elif "algorithm" in req_lower and user_skills.get("dsa", 0) > 60:
                matching.append("Algorithm Knowledge")
            elif "database" in req_lower and user_skills.get("database", 0) > 60:
                matching.append("Database Skills")
            elif "communication" in req_lower and user_skills.get("communication", 0) > 60:
                matching.append("Communication Skills")
        
        return matching
    
    def _get_skill_gaps(self, user_skills: Dict[str, float], 
                       requirements: List[str]) -> List[str]:
        """Get skill gaps for job requirements"""
        gaps = []
        for req in requirements:
            req_lower = req.lower()
            if "programming" in req_lower and user_skills.get("programming", 0) < 60:
                gaps.append("Programming Skills")
            elif "algorithm" in req_lower and user_skills.get("dsa", 0) < 60:
                gaps.append("Algorithm Knowledge")
            elif "database" in req_lower and user_skills.get("database", 0) < 60:
                gaps.append("Database Skills")
            elif "communication" in req_lower and user_skills.get("communication", 0) < 60:
                gaps.append("Communication Skills")
        
        return gaps
