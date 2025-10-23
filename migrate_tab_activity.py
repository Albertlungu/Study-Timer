#!/usr/bin/env python3
"""
Database migration script to add tab_activity table

Run this script to add the tab_activity table to an existing Study Timer database.
This is only needed for existing databases that were created before the tab activity feature.
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import DATABASE_PATH


def migrate_database():
    """Add tab_activity table to existing database"""

    try:
        # Connect to database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        print("🔄 Checking database schema...")

        # Check if tab_activity table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='tab_activity'
        """)

        if cursor.fetchone():
            print("✅ tab_activity table already exists!")
            conn.close()
            return

        # Create tab_activity table
        print("📝 Creating tab_activity table...")
        cursor.execute("""
            CREATE TABLE tab_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create index for tab_activity table
        cursor.execute("""
            CREATE INDEX idx_tab_activity_timestamp
            ON tab_activity(timestamp)
        """)

        conn.commit()
        conn.close()

        print("✅ Migration completed successfully!")
        print("📊 Tab activity tracking is now enabled.")
        print("\nThe tracker will now only count study time when the dashboard tab is active.")

    except Exception as e:
        print(f"❌ Error during migration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🎓 Study Timer Database Migration")
    print("=" * 40)
    print("\nAdding tab activity tracking support...\n")

    migrate_database()

    print("\n🚀 Migration complete!")
    print("\nNext steps:")
    print("1. Start the dashboard: python src/dashboard/app.py")
    print("2. Start the tracker: python src/main.py")
    print("\nThe tracker will now only count time when you're actively viewing the dashboard!")
