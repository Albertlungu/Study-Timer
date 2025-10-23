"""
Flask Dashboard Application - UPDATED
With project name tracking and improved time formatting
"""

from flask import Flask, render_template, jsonify, request
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
    """
    ✅ FIXED: Format seconds into hours and minutes, NOT just minutes
    Examples:
    - 3665 seconds = 1h 1m
    - 125 seconds = 2m
    - 7325 seconds = 2h 2m
    """
    if not seconds or seconds < 60:
        return "0m"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"
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


@app.route('/api/tab-activity', methods=['POST'])
def api_tab_activity():
    """Receive tab activity status from frontend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400

        is_active = data.get('is_active', True)
        timestamp = data.get('timestamp')

        if timestamp:
            # Convert timestamp string to datetime object
            from datetime import datetime
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                timestamp = datetime.now()

        # Store tab activity status in database
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tab_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO tab_activity (timestamp, is_active)
            VALUES (?, ?)
        """, (timestamp, is_active))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Tab activity recorded'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/tab-activity')
def api_get_tab_activity():
    """Get current tab activity status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the most recent tab activity status
        cursor.execute("""
            SELECT is_active, timestamp
            FROM tab_activity
            ORDER BY timestamp DESC
            LIMIT 1
        """)

        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({
                'is_active': result['is_active'],
                'timestamp': result['timestamp']
            })
        else:
            # Default to active if no data
            return jsonify({
                'is_active': True,
                'timestamp': None
            })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/today')
def api_today():
    """Get today's statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    
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
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT date, total_study_time, total_procrastination_time
        FROM daily_stats
        WHERE date BETWEEN ? AND ?
        ORDER BY date
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    current_date = week_ago
    
    for i in range(7):
        date_str = current_date.strftime('%Y-%m-%d')
        day_name = current_date.strftime('%a')
        
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
    """✅ UPDATED: Get recent study sessions WITH project names"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            app_name,
            window_title,
            file_path,
            website_url,
            project_name,
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
            'project_name': row['project_name'],  # ✅ NEW!
            'start_time': row['start_time'],
            'end_time': row['end_time'],
            'duration': row['duration'],
            'duration_formatted': format_duration(row['duration']),
            'is_study': row['is_study'],
            'is_procrastination': row['is_procrastination']
        })
    
    conn.close()
    return jsonify(data)


@app.route('/api/projects')
def api_projects():
    """✅ NEW: Get project time breakdown"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = date.today()
    week_ago = today - timedelta(days=6)
    
    cursor.execute("""
        SELECT 
            project_name,
            SUM(duration) as total_duration,
            COUNT(*) as session_count,
            MAX(start_time) as last_worked
        FROM sessions
        WHERE DATE(start_time) BETWEEN ? AND ? 
        AND project_name IS NOT NULL
        AND is_study = 1
        GROUP BY project_name
        ORDER BY total_duration DESC
        LIMIT 20
    """, (week_ago, today))
    
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        data.append({
            'project_name': row['project_name'],
            'duration': row['total_duration'],
            'duration_formatted': format_duration(row['total_duration']),
            'session_count': row['session_count'],
            'last_worked': row['last_worked']
        })
    
    conn.close()
    return jsonify(data)


@app.route('/api/export')
def api_export():
    """Export all data as CSV"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT app_name, window_title, file_path, website_url, project_name, start_time, end_time, duration, is_study, is_procrastination
            FROM sessions
            ORDER BY start_time DESC
        """)

        sessions = cursor.fetchall()

        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(['App Name', 'Window Title', 'File Path', 'Website URL', 'Project Name', 'Start Time', 'End Time', 'Duration (seconds)', 'Is Study', 'Is Procrastination'])

        for session in sessions:
            writer.writerow([
                session['app_name'] or '',
                session['window_title'] or '',
                session['file_path'] or '',
                session['website_url'] or '',
                session['project_name'] or '',
                session['start_time'] or '',
                session['end_time'] or '',
                session['duration'] or 0,
                session['is_study'] or 0,
                session['is_procrastination'] or 0
            ])

        conn.close()

        from flask import Response
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=studytime_export.csv'}
        )

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


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
    print("STUDYTIME DASHBOARD v2.1")
    print("=" * 60)
    print("\n✅ NEW FEATURES:")
    print("   • Project name tracking")
    print("   • Hours:Minutes time format")
    print("   • Improved pie chart colors")
    print("   • Tab activity tracking (tracks only when dashboard is active)")
    
    port = find_free_port(DASHBOARD_PORT)
    
    if port != DASHBOARD_PORT:
        print(f"\nWarning: Port {DASHBOARD_PORT} is busy, using port {port} instead")
    
    print(f"\nDashboard starting...")
    print(f"   Access at: http://localhost:{port}")
    print(f"   Or:        http://127.0.0.1:{port}")
    print("\nPress Ctrl+C to stop the dashboard\n")
    
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False, threaded=True)


if __name__ == '__main__':
    main()
