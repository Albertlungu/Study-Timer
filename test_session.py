#!/usr/bin/env python3
"""
Test script to manually create a Comet study session and verify it appears in the dashboard
"""

import sqlite3
import sys
from datetime import datetime, date
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

def test_session_creation():
    """Create a test Comet session and verify it works"""

    # Initialize database
    db_path = Path('data/study_data.db')
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if needed
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        app_name TEXT,
        window_title TEXT,
        file_path TEXT,
        website_url TEXT,
        start_time TEXT,
        end_time TEXT,
        duration INTEGER DEFAULT 0,
        is_study INTEGER DEFAULT 0,
        is_procrastination INTEGER DEFAULT 0
    )
    ''')

    # Create a test Comet session (like the user's scenario)
    now = datetime.now()
    session_data = {
        'app_name': 'Comet',
        'window_title': '2.0 Global climate SC 25-26 - Google Slides',
        'website_url': 'https://docs.google.com/presentation/d/1BZujzp4DWCPP2X7dEaNqR26VImlGTgtWExTru9xAHHY/edit?slide=id.g394b6218629_2_17#slide=id.g394b6218629_2_17',
        'start_time': now,
        'is_study': 1,
        'is_procrastination': 0,
        'duration': 300  # 5 minutes
    }

    print("=== CREATING TEST SESSION ===")
    print(f"App: {session_data['app_name']}")
    print(f"URL: {session_data['website_url']}")
    print(f"Study: {session_data['is_study']}")
    print(f"Duration: {session_data['duration']}s")

    # Insert the session
    cursor.execute("""
        INSERT INTO sessions
        (app_name, window_title, website_url, start_time, end_time, duration, is_study, is_procrastination)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_data['app_name'],
        session_data['window_title'],
        session_data['website_url'],
        session_data['start_time'],
        None,  # end_time - let dashboard calculate
        session_data['duration'],
        session_data['is_study'],
        session_data['is_procrastination']
    ))

    session_id = cursor.lastrowid
    print(f"Session created with ID: {session_id}")

    # Update daily stats
    today = date.today()
    cursor.execute("""
        SELECT
            SUM(CASE WHEN is_study = 1 THEN duration ELSE 0 END),
            SUM(CASE WHEN is_procrastination = 1 THEN duration ELSE 0 END),
            COUNT(*)
        FROM sessions WHERE DATE(start_time) = ?
    """, (today,))

    result = cursor.fetchone()
    study_time, procrastination_time, total_sessions = result

    print("\n=== UPDATING DAILY STATS ===")
    print(f"Study time: {study_time}s")
    print(f"Procrastination time: {procrastination_time}s")
    print(f"Total sessions: {total_sessions}")

    cursor.execute("""
        INSERT INTO daily_stats
        (date, total_study_time, total_procrastination_time, total_sessions, ib_quote)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            total_study_time = excluded.total_study_time,
            total_procrastination_time = excluded.total_procrastination_time,
            total_sessions = excluded.total_sessions,
            updated_at = CURRENT_TIMESTAMP
    """, (today, study_time or 0, procrastination_time or 0, total_sessions, "Test quote"))

    # Test dashboard API queries
    print("\n=== DASHBOARD API TESTS ===")

    # Test apps API
    cursor.execute("""
        SELECT
            app_name,
            SUM(duration) as total_duration,
            COUNT(*) as session_count
        FROM sessions
        WHERE DATE(start_time) = ? AND is_study = 1
        GROUP BY app_name
        ORDER BY total_duration DESC
    """, (today,))

    apps = cursor.fetchall()
    print(f"Apps API result: {apps}")

    # Test websites API
    cursor.execute("""
        SELECT
            website_url,
            SUM(duration) as total_duration,
            COUNT(*) as visit_count
        FROM sessions
        WHERE DATE(start_time) = ?
        AND is_study = 1
        AND website_url IS NOT NULL
        GROUP BY website_url
        ORDER BY total_duration DESC
    """, (today,))

    websites = cursor.fetchall()
    print(f"Websites API result: {websites}")

    # Test recent sessions
    cursor.execute("""
        SELECT
            app_name,
            window_title,
            website_url,
            start_time,
            duration,
            is_study,
            is_procrastination
        FROM sessions
        WHERE DATE(start_time) = ?
        ORDER BY start_time DESC
    """, (today,))

    sessions = cursor.fetchall()
    print(f"Recent sessions: {sessions}")

    conn.commit()
    conn.close()

    print("\n=== TEST COMPLETE ===")
    print("✅ Session created successfully")
    print("✅ Dashboard APIs tested")
    print("🔄 Check the dashboard at http://localhost:5000")
    print("   You should see Comet listed in apps and Google Docs in websites")

if __name__ == "__main__":
    test_session_creation()
