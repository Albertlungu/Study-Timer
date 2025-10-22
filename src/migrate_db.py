"""
Database migration script

Adds project_name field to sessions table
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import DATABASE_PATH


def migrate_database():
    """Add project_name column to sessions table"""
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check if project_name column exists
    cursor.execute("PRAGMA table_info(sessions)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'project_name' not in columns:
        print("Adding project_name column to sessions table...")
        cursor.execute("""
            ALTER TABLE sessions ADD COLUMN project_name TEXT
        """)
        conn.commit()
        print("✅ Successfully added project_name column!")
    else:
        print("✅ project_name column already exists!")
    
    conn.close()
    print("\n🚀 Database migration complete!")


if __name__ == "__main__":
    print("🎓 Migrating Study Timer Database...")
    print("=" * 50)
    migrate_database()
