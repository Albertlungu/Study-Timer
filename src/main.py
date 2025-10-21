"""
Main Study Timer Daemon
Tracks your study sessions automatically
"""

import sqlite3
import time
import sys
import logging
from datetime import datetime, date
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent))

from config import (
    DATABASE_PATH, TRACKING_INTERVAL, IDLE_TIMEOUT,
    STUDY_APPS, STUDY_WEBSITES, PROCRASTINATION_WEBSITES,
    LOG_FILE, LOG_LEVEL, IB_QUOTES
)
from trackers import AppTracker, BrowserTracker, FileTracker


class StudyTimer:
    """Main tracking daemon"""
    
    def __init__(self):
        self.app_tracker = AppTracker()
        self.browser_tracker = BrowserTracker()
        self.file_tracker = FileTracker()
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.current_session = None
        self.session_start = None
        self.setup_logging()
        self.logger.info("Study Timer initialized!")
    
    def setup_logging(self):
        """Setup logging"""
        LOG_FILE.parent.mkdir(exist_ok=True)
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('StudyTimer')
    
    def is_study_activity(self, app_name, url=None):
        """Check if activity is study-related"""
        if app_name in STUDY_APPS:
            if self.browser_tracker.is_browser(app_name) and url:
                category = self.browser_tracker.categorize_website(
                    url, STUDY_WEBSITES, PROCRASTINATION_WEBSITES
                )
                if category == 'study':
                    return (True, False)
                elif category == 'procrastination':
                    return (False, True)
                return (False, False)
            return (True, False)
        return (False, False)
    
    def log_activity(self, activity_data):
        """Log activity to database"""
        try:
            self.cursor.execute("""
                INSERT INTO activity_log 
                (timestamp, app_name, window_title, file_path, website_url, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                activity_data['timestamp'],
                activity_data['app_name'],
                activity_data.get('window_title'),
                activity_data.get('file_path'),
                activity_data.get('url'),
                True
            ))
            self.conn.commit()
        except Exception as e:
            self.logger.error(f"Error logging: {e}")
    
    def start_new_session(self, activity_data, is_study, is_procrastination):
        """Start tracking session"""
        try:
            self.cursor.execute("""
                INSERT INTO sessions 
                (app_name, window_title, file_path, website_url, start_time, is_study, is_procrastination)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                activity_data['app_name'],
                activity_data.get('window_title'),
                activity_data.get('file_path'),
                activity_data.get('url'),
                activity_data['timestamp'],
                is_study,
                is_procrastination
            ))
            self.conn.commit()
            self.current_session = self.cursor.lastrowid
            self.session_start = activity_data['timestamp']
            
            status = "STUDYING" if is_study else "PROCRASTINATING" if is_procrastination else "WORKING"
            self.logger.info(f"New session: {status} - {activity_data['app_name']}")
        except Exception as e:
            self.logger.error(f"Error starting session: {e}")
    
    def end_current_session(self, end_time):
        """End current session"""
        if not self.current_session:
            return
        try:
            duration = int((end_time - self.session_start).total_seconds())
            self.cursor.execute("""
                UPDATE sessions SET end_time = ?, duration = ? WHERE id = ?
            """, (end_time, duration, self.current_session))
            self.conn.commit()
            self.logger.info(f"Session ended: {duration}s")
            self.current_session = None
            self.session_start = None
        except Exception as e:
            self.logger.error(f"Error ending session: {e}")
    
    def update_daily_stats(self):
        """Update daily statistics"""
        try:
            today = date.today()
            self.cursor.execute("""
                SELECT 
                    SUM(CASE WHEN is_study = 1 THEN duration ELSE 0 END),
                    SUM(CASE WHEN is_procrastination = 1 THEN duration ELSE 0 END),
                    COUNT(*)
                FROM sessions WHERE DATE(start_time) = ?
            """, (today,))
            
            result = self.cursor.fetchone()
            study_time, procrastination_time, total_sessions = result
            
            ib_quote = random.choice(IB_QUOTES)
            
            self.cursor.execute("""
                INSERT INTO daily_stats 
                (date, total_study_time, total_procrastination_time, total_sessions, ib_quote)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    total_study_time = excluded.total_study_time,
                    total_procrastination_time = excluded.total_procrastination_time,
                    total_sessions = excluded.total_sessions,
                    ib_quote = excluded.ib_quote,
                    updated_at = CURRENT_TIMESTAMP
            """, (today, study_time or 0, procrastination_time or 0, total_sessions, ib_quote))
            self.conn.commit()
        except Exception as e:
            self.logger.error(f"Error updating stats: {e}")
    
    def run(self):
        """Main loop"""
        self.logger.info("Starting study tracking...")
        update_counter = 0
        
        try:
            while True:
                activity = self.app_tracker.get_current_activity()
                app_name = activity['app_name']
                
                if self.app_tracker.is_idle(IDLE_TIMEOUT):
                    if self.current_session:
                        self.end_current_session(datetime.now())
                    time.sleep(TRACKING_INTERVAL)
                    continue
                
                url = None
                if self.browser_tracker.is_browser(app_name):
                    browser_activity = self.browser_tracker.get_browser_activity(app_name)
                    url = browser_activity.get('url')
                
                is_study, is_procrastination = self.is_study_activity(app_name, url)
                
                activity_data = {
                    'timestamp': activity['timestamp'],
                    'app_name': app_name,
                    'window_title': activity['window_title'],
                    'file_path': activity['file_path'],
                    'url': url
                }
                
                self.log_activity(activity_data)
                
                if activity['is_new_session']:
                    if self.current_session:
                        self.end_current_session(activity['timestamp'])
                    if is_study or is_procrastination:
                        self.start_new_session(activity_data, is_study, is_procrastination)
                
                update_counter += 1
                if update_counter >= 10:
                    self.update_daily_stats()
                    update_counter = 0
                
                time.sleep(TRACKING_INTERVAL)
        
        except KeyboardInterrupt:
            self.logger.info("Stopping tracker...")
            if self.current_session:
                self.end_current_session(datetime.now())
            self.update_daily_stats()
            self.conn.close()
            self.logger.info("Tracker stopped!")
        
        except Exception as e:
            self.logger.error(f"Error: {e}")
            if self.current_session:
                self.end_current_session(datetime.now())
            self.conn.close()
            raise


def main():
    """Entry point"""
    print("=" * 60)
    print("📚 STUDY TIMER - Procrastination Detector 3000")
    print("=" * 60)
    print("\n🎯 Mission: Track your study time automatically")
    print("⚠️  Reality: Reveal how much you actually procrastinate\n")
    print("💡 Grant Accessibility permissions in System Preferences!")
    print("   (Security & Privacy → Privacy → Accessibility)\n")
    
    timer = StudyTimer()
    timer.run()


if __name__ == "__main__":
    main()
