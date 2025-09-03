# config.py
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    
    # Database
    DATABASE_PATH: str = "preptor.db"
    
    # Models
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Assessment Configuration
    APTITUDE_QUESTIONS: int = 20
    TECHNICAL_QUESTIONS: int = 15
    MOCK_INTERVIEW_DURATION: int = 30  
    
    # Scoring Weights
    SKILL_WEIGHTS: Dict[str, float] = field(default_factory=lambda: {
        "aptitude": 0.25,
        "technical": 0.35,
        "communication": 0.20,
        "resume": 0.20
    })
    
    # Company Lists
    TARGET_COMPANIES: List[str] = field(default_factory=lambda: [
        "TCS", "Infosys", "Wipro", "Amazon", "Google", 
        "Microsoft", "Accenture", "IBM", "Cognizant", "HCL"
    ])

config = Config()