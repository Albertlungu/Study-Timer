#!/usr/bin/env python3
"""
Debug script to test the exact classification and session creation logic
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'src'))

def debug_classification():
    """Debug the exact classification logic step by step"""

    from config import STUDY_APPS, PROCRASTINATION_APPS, STUDY_WEBSITES, PROCRASTINATION_WEBSITES
    from trackers.browser_tracker import BrowserTracker

    # Simulate the exact activity from user's logs
    app_name = 'Comet'
    url = 'https://docs.google.com/presentation/d/1BZujzp4DWCPP2X7dEaNqR26VImlGTgtWExTru9xAHHY/edit?slide=id.g394b6218629_2_17#slide=id.g394b6218629_2_17'
    window_title = '2.0 Global climate SC 25-26 - Google Slides'

    print("=== STEP-BY-STEP DEBUG ===")
    print(f"App: {app_name}")
    print(f"URL: {url}")
    print(f"Title: {window_title}")
    print()

    # Step 1: Check if procrastination app
    print("1. Checking PROCRASTINATION_APPS...")
    if app_name in PROCRASTINATION_APPS:
        print(f"   ❌ {app_name} is in PROCRASTINATION_APPS")
        return (False, True)
    else:
        print(f"   {app_name} is NOT in PROCRASTINATION_APPS")

    # Step 2: Check if study app
    print("\n2. Checking STUDY_APPS...")
    if app_name in STUDY_APPS:
        print(f"   {app_name} is in STUDY_APPS")

        # Step 3: Check if browser
        tracker = BrowserTracker()
        is_browser = tracker.is_browser(app_name)
        print(f"\n3. Checking if browser: {is_browser}")

        if is_browser and url:
            print("   Browser with URL detected")

            # Step 4: Categorize URL
            print("\n4. Categorizing URL...")
            category = tracker.categorize_website(url, STUDY_WEBSITES, PROCRASTINATION_WEBSITES)
            print(f"   URL category: {category}")

            if category == 'study':
                print("   URL is STUDY")
                return (True, False)
            elif category == 'procrastination':
                print("   ❌ URL is PROCRASTINATION")
                return (False, True)
            else:
                print("   ❌ URL is UNKNOWN")
                return (False, False)
        else:
            print("   Non-browser study app")
            return (True, False)
    else:
        print(f"   ❌ {app_name} is NOT in STUDY_APPS")
        return (False, False)

def test_database_creation():
    """Test if we can create and query sessions"""

    import sqlite3

    # Create database
    db_path = Path('data/study_data.db')
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
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

    # Test classification
    is_study, is_procrastination = debug_classification()

    print("\n=== SESSION CREATION TEST ===")
    print(f'Result: is_study={is_study}, is_procrastination={is_procrastination}')
    print(f'Session would be created: {is_study or is_procrastination}')

    if is_study or is_procrastination:
        print("Would create session")

        # Create test session
        now = datetime.now()
        cursor.execute("""
            INSERT INTO sessions
            (app_name, window_title, website_url, start_time, is_study, is_procrastination, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (app_name, window_title, url, now, is_study, is_procrastination, 300))

        session_id = cursor.lastrowid
        print(f"Session created with ID: {session_id}")

        # Test dashboard queries
        print("\n=== DASHBOARD QUERY TESTS ===")

        # Apps query
        cursor.execute("""
            SELECT app_name, SUM(duration) as total_duration, COUNT(*) as session_count
            FROM sessions WHERE is_study = 1 GROUP BY app_name ORDER BY total_duration DESC
        """)
        apps = cursor.fetchall()
        print(f"Apps query result: {apps}")

        # Websites query
        cursor.execute("""
            SELECT website_url, SUM(duration) as total_duration, COUNT(*) as visit_count
            FROM sessions WHERE is_study = 1 AND website_url IS NOT NULL
            GROUP BY website_url ORDER BY total_duration DESC
        """)
        websites = cursor.fetchall()
        print(f"Websites query result: {websites}")

    else:
        print("❌ Would NOT create session")

    conn.commit()
    conn.close()

    print("\n=== TEST COMPLETE ===")
    print("If session was created, check dashboard at http://localhost:5000")

if __name__ == "__main__":
    test_database_creation()
