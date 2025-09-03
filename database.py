# database.py
import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "preptor.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                branch TEXT NOT NULL,
                year INTEGER NOT NULL,
                preferred_companies TEXT,  -- JSON array
                dream_role TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Skill profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skill_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                aptitude_score REAL DEFAULT 0,
                technical_score REAL DEFAULT 0,
                communication_score REAL DEFAULT 0,
                resume_score REAL DEFAULT 0,
                overall_score REAL DEFAULT 0,
                skill_matrix TEXT,  -- JSON
                weak_areas TEXT,    -- JSON array
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Assessment results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                assessment_type TEXT NOT NULL,
                score REAL NOT NULL,
                details TEXT,  -- JSON
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Learning progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic TEXT NOT NULL,
                progress_percentage REAL DEFAULT 0,
                resources_completed TEXT,  -- JSON array
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Job matches table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                fit_score REAL NOT NULL,
                job_url TEXT,
                requirements TEXT,  -- JSON
                matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """Create a new user and return user ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (username, email, branch, year, preferred_companies, dream_role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_data['username'],
            user_data['email'],
            user_data['branch'],
            user_data['year'],
            json.dumps(user_data.get('preferred_companies', [])),
            user_data.get('dream_role', '')
        ))
        
        user_id = cursor.lastrowid
        
        # Create initial skill profile
        cursor.execute("""
            INSERT INTO skill_profiles (user_id, skill_matrix, weak_areas)
            VALUES (?, ?, ?)
        """, (user_id, json.dumps({}), json.dumps([])))
        
        conn.commit()
        conn.close()
        return user_id
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
            user['preferred_companies'] = json.loads(user.get('preferred_companies', '[]'))
            conn.close()
            return user
        
        conn.close()
        return None
    
    def update_skill_profile(self, user_id: int, scores: Dict[str, float], 
                           skill_matrix: Dict[str, Any], weak_areas: List[str]):
        """Update user's skill profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        overall_score = sum(scores[key] * config.SKILL_WEIGHTS[key] for key in scores.keys())
        
        cursor.execute("""
            UPDATE skill_profiles SET
                aptitude_score = ?, technical_score = ?, 
                communication_score = ?, resume_score = ?,
                overall_score = ?, skill_matrix = ?, weak_areas = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, (
            scores.get('aptitude', 0), scores.get('technical', 0),
            scores.get('communication', 0), scores.get('resume', 0),
            overall_score, json.dumps(skill_matrix), json.dumps(weak_areas), user_id
        ))
        
        conn.commit()
        conn.close()
    
    def save_assessment_result(self, user_id: int, assessment_type: str, 
                             score: float, details: Dict[str, Any]):
        """Save assessment results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO assessments (user_id, assessment_type, score, details)
            VALUES (?, ?, ?, ?)
        """, (user_id, assessment_type, score, json.dumps(details)))
        
        conn.commit()
        conn.close()
    
    def get_user_skill_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's current skill profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM skill_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            profile = dict(zip(columns, row))
            profile['skill_matrix'] = json.loads(profile.get('skill_matrix', '{}'))
            profile['weak_areas'] = json.loads(profile.get('weak_areas', '[]'))
            conn.close()
            return profile
        
        conn.close()
        return None