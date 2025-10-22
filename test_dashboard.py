#!/usr/bin/env python3
"""
Test script to verify StudyTime dashboard functionality
"""

import requests
import json
import time
import sqlite3
from datetime import datetime, timedelta

def test_api_endpoint(url, description):
    """Test an API endpoint"""
    try:
        response = requests.get(url, timeout=5)
        print(f"{description}: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {description}: {e}")
        return None

def add_sample_data():
    """Add some sample data to the database for testing"""
    conn = sqlite3.connect('data/study_data.db')
    cursor = conn.cursor()

    # Check if we already have data
    cursor.execute('SELECT COUNT(*) FROM sessions')
    count = cursor.fetchone()[0]

    if count > 10:  # Already have enough data
        print("Database already has sufficient data")
        conn.close()
        return

    print(f"Adding sample data (current sessions: {count})")

    # Add sample sessions
    base_time = datetime.now() - timedelta(hours=24)

    sample_sessions = [
        ('Visual Studio Code', 'main.py - StudyTimer', '/Users/student/projects/studytimer/main.py', None, 1, 0, 3600, base_time.strftime('%Y-%m-%d %H:%M:%S')),
        ('Chrome', 'GitHub - StudyTimer', None, 'https://github.com/student/studytimer', 1, 0, 1800, (base_time + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:%S')),
        ('Notion', 'Study Notes', None, 'https://notion.so/workspace/study-notes', 1, 0, 2700, (base_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')),
        ('YouTube', 'Educational Content', None, 'https://youtube.com/watch?v=abc123', 0, 1, 600, (base_time + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')),
        ('VS Code', 'dashboard.py', '/Users/student/projects/studytimer/dashboard.py', None, 1, 0, 2400, (base_time + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')),
    ]

    for session in sample_sessions:
        cursor.execute('''
            INSERT INTO sessions (app_name, window_title, file_path, website_url, is_study, is_procrastination, duration, start_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', session)

    # Add daily stats
    cursor.execute('''
        INSERT OR REPLACE INTO daily_stats (date, total_study_time, total_procrastination_time, total_sessions)
        VALUES (?, ?, ?, ?)
    ''', (base_time.strftime('%Y-%m-%d'), 8700, 600, 5))

    conn.commit()
    conn.close()
    print("Sample data added successfully")

def main():
    print("🧪 Testing StudyTime Dashboard")
    print("=" * 50)

    # Add sample data if needed
    add_sample_data()

    # Test API endpoints
    base_url = "http://localhost:5000"

    # Wait a moment for dashboard to start
    print("\n📡 Testing API endpoints...")
    time.sleep(2)

    endpoints = [
        (f"{base_url}/api/today", "Today Stats"),
        (f"{base_url}/api/recent_sessions", "Recent Sessions"),
        (f"{base_url}/api/apps", "App Stats"),
        (f"{base_url}/api/websites/study", "Study Websites"),
        (f"{base_url}/api/stats/summary", "Summary Stats"),
    ]

    results = {}
    for url, desc in endpoints:
        data = test_api_endpoint(url, desc)
        results[desc] = data

    print("\n📊 Data Summary:")
    print(f"   Today study time: {results.get('Today Stats', {}).get('study_time_formatted', 'N/A')}")
    print(f"   Sessions today: {results.get('Today Stats', {}).get('total_sessions', 'N/A')}")
    print(f"   Recent sessions: {len(results.get('Recent Sessions', []))}")
    print(f"   Study apps: {len(results.get('App Stats', []))}")
    print(f"   Study websites: {len(results.get('Study Websites', []))}")

    print("\nDashboard test complete!")
    print("   If dashboard is running, visit: http://localhost:5000")

if __name__ == "__main__":
    main()
