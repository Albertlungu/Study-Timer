"""
Database migration: Add project_name column to sessions table
Run this to add the project_name tracking feature
"""

import sqlite3
import sys
from pathlib import Path

# Update these paths to match your setup
DATABASE_PATH = Path(__file__).parent.parent / "data" / "study_data.db"

def migrate():
    """Add project_name column to sessions table"""
    
    print("🔧 Starting database migration...")
    print(f"📍 Database: {DATABASE_PATH}")
    
    if not DATABASE_PATH.exists():
        print("❌ Database not found! Please run init_db.py first.")
        return False
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(sessions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'project_name' in columns:
            print("✅ Column 'project_name' already exists!")
            conn.close()
            return True
        
        # Add the column
        print("📝 Adding 'project_name' column to sessions table...")
        cursor.execute("""
            ALTER TABLE sessions 
            ADD COLUMN project_name TEXT
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Migration completed successfully!")
        print("\n🚀 Your database now tracks project names!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: Add Project Name Tracking")
    print("=" * 60)
    print()
    migrate()
