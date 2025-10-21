"""
Flask Dashboard Application

A beautiful web interface to view your study statistics.
Because staring at raw database queries is not fun.
"""

from flask import Flask, render_template, jsonify
import sqlite3
import sys
from pathlib import Path
from datetime import datetime, timedelta, date
import os

sys.path.append(str(Path(__file__).parent.parent))

from config import DATABASE_PATH, DASHBOARD_PORT, DASHBOARD_HOST, IB_QUOTES
import random

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def format_duration(seconds):
    """Format seconds into human readable duration"""
    if not seconds:
        return "0m"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def extract_domain(url):
    """Extract domain from URL"""
    if not url:
        return None
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '')
    except:
        return url


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/today')
def api_today():
    """Get today's statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    
    # Get today's stats
    cursor.execute("""
        SELECT * FROM daily_stats WHERE date = ?
    """, (today,))
    
    stats = cursor.fetchone()
    
    if stats:
        data = {
            'study_time': stats['total_study_time'],
            'study_time_formatted': format_duration(stats['total_study_time']),
            'procrastination_time': stats['total_procrastination_time'],
            'procrastination_time_formatted': format_duration(stats['total_procrastination_time']),
            'total_sessions': stats['total_sessions'],
            'most_used_app': stats['most_used_app'],
            'ib_quote': stats['ib_quote']
        }
    else:
        data = {
            'study_time': 0,
            'study_time_formatted': '0m',
            'procrastination_time': 0,
            'procrastination_time_formatted': '0m',
            'total_sessions': 0,
            'most_used_app': None,
            'ib_quote': random.choice(IB_QUOTES)
        }
    
    conn.close()
    return jsonify(data)


@app.route('/api/week')
def api_week():
    """Get this week's statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get last 7 days
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT date, total_study_time, total_procrastination_time
        FROM daily_stats
        WHERE date BETWEEN ? AND ?
        ORDER BY date
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    # Create data for all 7 days (fill in missing days with 0)
    data = []
    current_date = week_ago
    
    for i in range(7):
        date_str = current_date.strftime('%Y-%m-%d')
        day_name = current_date.strftime('%a')
        
        # Find matching row
        matching_row = next((row for row in rows if row['date'] == date_str), None)
        
        if matching_row:
            data.append({
                'date': date_str,
                'day': day_name,
                'study_time': matching_row['total_study_time'],
                'procrastination_time': matching_row['total_procrastination_time']
            })
        else:
            data.append({
                'date': date_str,
                'day': day_name,
                'study_time': 0,
                'procrastination_time': 0
            })
        
        current_date += timedelta(days=1)
    
    conn.close()
    return jsonify(data)


@app.route('/api/apps')
def api_apps():
    """Get app usage statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT 
            app_name,
            SUM(duration) as total_duration,
            COUNT(*) as session_count
        FROM sessions
        WHERE DATE(start_time) BETWEEN ? AND ? AND is_study = 1
        GROUP BY app_name
        ORDER BY total_duration DESC
        LIMIT 10
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'app_name': row['app_name'],
            'duration': row['total_duration'],
            'duration_formatted': format_duration(row['total_duration']),
            'session_count': row['session_count']
        })
    
    conn.close()
    return jsonify(data)


@app.route('/api/websites/study')
def api_websites_study():
    """Get study websites breakdown"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT 
            website_url,
            SUM(duration) as total_duration,
            COUNT(*) as visit_count
        FROM sessions
        WHERE DATE(start_time) BETWEEN ? AND ? 
        AND is_study = 1 
        AND website_url IS NOT NULL
        GROUP BY website_url
        ORDER BY total_duration DESC
        LIMIT 15
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        domain = extract_domain(row['website_url'])
        if domain:
            data.append({
                'domain': domain,
                'url': row['website_url'],
                'duration': row['total_duration'],
                'duration_formatted': format_duration(row['total_duration']),
                'visit_count': row['visit_count']
            })
    
    conn.close()
    return jsonify(data)


@app.route('/api/websites/procrastination')
def api_websites_procrastination():
    """Get procrastination websites breakdown"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT 
            website_url,
            SUM(duration) as total_duration,
            COUNT(*) as visit_count
        FROM sessions
        WHERE DATE(start_time) BETWEEN ? AND ? 
        AND is_procrastination = 1 
        AND website_url IS NOT NULL
        GROUP BY website_url
        ORDER BY total_duration DESC
        LIMIT 15
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        domain = extract_domain(row['website_url'])
        if domain:
            data.append({
                'domain': domain,
                'url': row['website_url'],
                'duration': row['total_duration'],
                'duration_formatted': format_duration(row['total_duration']),
                'visit_count': row['visit_count']
            })
    
    conn.close()
    return jsonify(data)


@app.route('/api/files')
def api_files():
    """Get recently worked on files"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT 
            file_path,
            app_name,
            SUM(duration) as total_duration,
            MAX(start_time) as last_worked
        FROM sessions
        WHERE DATE(start_time) BETWEEN ? AND ? 
        AND file_path IS NOT NULL 
        AND is_study = 1
        GROUP BY file_path, app_name
        ORDER BY last_worked DESC
        LIMIT 20
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'file_path': row['file_path'],
            'app_name': row['app_name'],
            'duration': row['total_duration'],
            'duration_formatted': format_duration(row['total_duration']),
            'last_worked': row['last_worked']
        })
    
    conn.close()
    return jsonify(data)


@app.route('/api/recent_sessions')
def api_recent_sessions():
    """Get recent study sessions"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            app_name,
            window_title,
            file_path,
            website_url,
            start_time,
            end_time,
            duration,
            is_study,
            is_procrastination
        FROM sessions
        WHERE start_time >= datetime('now', '-1 day')
        ORDER BY start_time DESC
        LIMIT 50
    """)
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        domain = extract_domain(row['website_url']) if row['website_url'] else None
        
        data.append({
            'app_name': row['app_name'],
            'window_title': row['window_title'],
            'file_path': row['file_path'],
            'website_url': row['website_url'],
            'website_domain': domain,
            'start_time': row['start_time'],
            'end_time': row['end_time'],
            'duration': row['duration'],
            'duration_formatted': format_duration(row['duration']),
            'is_study': row['is_study'],
            'is_procrastination': row['is_procrastination']
        })
    
    conn.close()
    return jsonify(data)


@app.route('/api/stats/summary')
def api_stats_summary():
    """Get overall summary statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total all-time study time
    cursor.execute("""
        SELECT SUM(total_study_time) as total_study
        FROM daily_stats
    """)
    total_study = cursor.fetchone()['total_study'] or 0
    
    # Average daily study time
    cursor.execute("""
        SELECT AVG(total_study_time) as avg_study
        FROM daily_stats
        WHERE total_study_time > 0
    """)
    avg_study = cursor.fetchone()['avg_study'] or 0
    
    # Most productive day
    cursor.execute("""
        SELECT date, total_study_time
        FROM daily_stats
        ORDER BY total_study_time DESC
        LIMIT 1
    """)
    best_day = cursor.fetchone()
    
    # Study streak (consecutive days with study time)
    cursor.execute("""
        SELECT date, total_study_time
        FROM daily_stats
        ORDER BY date DESC
    """)
    days = cursor.fetchall()
    
    streak = 0
    for day in days:
        if day['total_study_time'] > 0:
            streak += 1
        else:
            break
    
    data = {
        'total_study_time': total_study,
        'total_study_time_formatted': format_duration(total_study),
        'avg_daily_study': int(avg_study),
        'avg_daily_study_formatted': format_duration(int(avg_study)),
        'best_day_date': best_day['date'] if best_day else None,
        'best_day_time': best_day['total_study_time'] if best_day else 0,
        'best_day_time_formatted': format_duration(best_day['total_study_time']) if best_day else '0m',
        'current_streak': streak
    }
    
    conn.close()
    return jsonify(data)


def find_free_port(start_port=5000):
    """Find a free port starting from start_port"""
    import socket
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return start_port


def main():
    """Run the dashboard"""
    print("=" * 60)
    print("📊 STUDY TIMER DASHBOARD")
    print("=" * 60)
    
    # Check if port is available, if not find a free one
    port = find_free_port(DASHBOARD_PORT)
    
    if port != DASHBOARD_PORT:
        print(f"\n⚠️  Port {DASHBOARD_PORT} is busy, using port {port} instead")
    
    print(f"\n🌐 Dashboard starting...")
    print(f"   Access at: http://localhost:{port}")
    print(f"   Or:        http://127.0.0.1:{port}")
    print("📈 View your study stats in real-time!")
    print("\n💡 Tip: Keep the tracker running (main.py) to collect data")
    print("\n💡 If you get a 403 error:")
    print("   1. Run: chmod +x kill_dashboard.sh && ./kill_dashboard.sh")
    print("   2. Try again")
    print("\n⚠️  Press Ctrl+C to stop the dashboard\n")
    
    # Run with proper settings
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, threaded=True)


if __name__ == '__main__':
    main()
