# app/database.py
import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path="language_learning.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                user_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT DEFAULT '{}'
            )
        ''')
        
        # Content history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content_type TEXT NOT NULL,
                input_text TEXT,
                input_language TEXT,
                output_language TEXT,
                generated_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_sessions (user_id)
            )
        ''')
        
        # File uploads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                file_id TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                transcription TEXT,
                language_detected TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_sessions (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def update_user_session(self, user_id: str, preferences: dict = None):
        """Update or create user session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_sessions (user_id, preferences)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                last_active = CURRENT_TIMESTAMP,
                preferences = COALESCE(?, preferences)
        ''', (user_id, json.dumps(preferences or {}), json.dumps(preferences or {})))
        
        conn.commit()
        conn.close()
    
    def save_content_history(self, user_id: str, content_data: dict):
        """Save generated content to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO content_history 
            (user_id, content_type, input_text, input_language, output_language, generated_content)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            content_data.get('content_type'),
            content_data.get('input_text'),
            content_data.get('input_language'),
            content_data.get('output_language'),
            content_data.get('generated_content')
        ))
        
        conn.commit()
        conn.close()
    
    def get_user_history(self, user_id: str, limit: int = 10):
        """Get user's content history"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM content_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

# Initialize database
db = Database()