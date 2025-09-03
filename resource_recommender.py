# resource_recommender.py
import requests
from typing import List, Dict, Any
from groq_client import GroqClient
from config import config

class ResourceRecommender:
    def __init__(self, youtube_api_key: str = ""):
        self.youtube_api_key = youtube_api_key
        self.groq_client = GroqClient(config.GROQ_API_KEY)
    
    def get_youtube_resources(self, topic: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Fetch YouTube resources for a topic"""
        if not self.youtube_api_key:
            # Return mock data if no API key
            return [
                {
                    "title": f"Complete {topic} Tutorial",
                    "url": f"https://youtube.com/watch?v=example_{topic.lower().replace(' ', '_')}",
                    "description": f"Comprehensive tutorial covering {topic} concepts"
                }
            ]
        
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": f"{topic} tutorial programming placement",
                "type": "video",
                "order": "relevance",
                "maxResults": max_results,
                "key": self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            resources = []
            for item in data.get("items", []):
                resources.append({
                    "title": item["snippet"]["title"],
                    "url": f"https://youtube.com/watch?v={item['id']['videoId']}",
                    "description": item["snippet"]["description"][:200] + "..."
                })
            
            return resources
        except Exception as e:
            print(f"Error fetching YouTube resources: {e}")
            return []
    
    def recommend_resources(self, skill_gaps: List[str], user_level: str = "beginner") -> Dict[str, List[Dict[str, str]]]:
        """Recommend learning resources for skill gaps"""
        recommendations = {}
        
        for gap in skill_gaps:
            resources = []
            
            # YouTube videos
            youtube_resources = self.get_youtube_resources(gap)
            resources.extend(youtube_resources)
            
            # Additional curated resources
            if "DSA" in gap or "Data Structures" in gap:
                resources.extend([
                    {
                        "title": "LeetCode - Practice Problems",
                        "url": "https://leetcode.com",
                        "description": "Platform for coding practice with company-specific questions"
                    },
                    {
                        "title": "GeeksforGeeks DSA Course",
                        "url": "https://geeksforgeeks.org/data-structures",
                        "description": "Comprehensive data structures and algorithms tutorials"
                    }
                ])
            
            if "DBMS" in gap:
                resources.extend([
                    {
                        "title": "W3Schools SQL Tutorial",
                        "url": "https://w3schools.com/sql",
                        "description": "Interactive SQL learning platform"
                    },
                    {
                        "title": "SQLBolt - Interactive SQL Lessons",
                        "url": "https://sqlbolt.com",
                        "description": "Learn SQL with interactive exercises"
                    }
                ])
            
            if "Communication" in gap:
                resources.extend([
                    {
                        "title": "Toastmasters International",
                        "url": "https://toastmasters.org",
                        "description": "Public speaking and leadership skills development"
                    },
                    {
                        "title": "Coursera - Business English",
                        "url": "https://coursera.org/learn/business-english",
                        "description": "Professional communication skills course"
                    }
                ])
            
            recommendations[gap] = resources
        
        return recommendations
    
    def get_company_specific_resources(self, company: str) -> Dict[str, List[str]]:
        """Get company-specific preparation resources"""
        company_resources = {
            "TCS": {
                "coding_pattern": ["Array manipulation", "String processing", "Basic algorithms"],
                "technical_topics": ["C/C++/Java basics", "DBMS fundamentals", "Operating Systems"],
                "interview_tips": [
                    "Focus on basic programming concepts",
                    "Practice TCS CodeVita previous problems",
                    "Prepare for HR questions about TCS values"
                ]
            },
            "Infosys": {
                "coding_pattern": ["Logic building", "Mathematics", "Pattern recognition"],
                "technical_topics": ["OOP concepts", "Database queries", "System design basics"],
                "interview_tips": [
                    "Strong foundation in mathematics",
                    "Practice Infosys Hackerrank questions",
                    "Focus on communication skills"
                ]
            },
            "Amazon": {
                "coding_pattern": ["Dynamic programming", "Graph algorithms", "System design"],
                "technical_topics": ["AWS basics", "Scalability", "Leadership principles"],
                "interview_tips": [
                    "Study Amazon's 14 leadership principles",
                    "Practice LeetCode medium/hard problems",
                    "Prepare STAR method examples"
                ]
            },
            "Google": {
                "coding_pattern": ["Algorithm optimization", "Complex data structures", "Math problems"],
                "technical_topics": ["System design", "Machine learning", "Distributed systems"],
                "interview_tips": [
                    "Focus on problem-solving approach",
                    "Practice coding interviews daily",
                    "Study system design fundamentals"
                ]
            }
        }
        
        return company_resources.get(company, {
            "coding_pattern": ["Basic programming", "Data structures", "Algorithms"],
            "technical_topics": ["Programming fundamentals", "Database basics", "System concepts"],
            "interview_tips": ["Practice coding problems", "Improve communication", "Research company culture"]
        })