"""
Database initialization script

Creates the SQLite database schema for tracking study sessions.
Run this once before starting the tracker.
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import DATABASE_PATH, DATA_DIR, LOGS_DIR


def init_database():
    """Initialize the study tracking database"""
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Connect to database (creates file if it doesn't exist)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT NOT NULL,
            window_title TEXT,
            file_path TEXT,
            website_url TEXT,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            duration INTEGER DEFAULT 0,
            is_study BOOLEAN DEFAULT 1,
            is_procrastination BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create activity_log table for detailed tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP NOT NULL,
            app_name TEXT NOT NULL,
            window_title TEXT,
            file_path TEXT,
            website_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create daily_stats table for quick lookups
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL UNIQUE,
            total_study_time INTEGER DEFAULT 0,
            total_procrastination_time INTEGER DEFAULT 0,
            total_sessions INTEGER DEFAULT 0,
            apps_used TEXT,
            most_used_app TEXT,
            files_worked_on TEXT,
            ib_quote TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indices for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_start_time 
        ON sessions(start_time)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_app_name 
        ON sessions(app_name)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_activity_timestamp 
        ON activity_log(timestamp)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_daily_stats_date 
        ON daily_stats(date)
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print(f"📍 Location: {DATABASE_PATH}")
    print("\n🚀 Ready to track your study sessions!")
    print("\nNext steps:")
    print("1. Run: python src/main.py (to start tracking)")
    print("2. Run: python src/dashboard/app.py (to view your stats)")


if __name__ == "__main__":
    print("🎓 Initializing Study Timer Database...")
    print("=" * 50)
    init_database()
