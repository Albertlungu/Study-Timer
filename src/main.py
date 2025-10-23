"""
Main Study Timer Daemon - UPDATED WITH PROJECT NAME TRACKING
Tracks your study sessions automatically with project name extraction
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
    STUDY_APPS, STUDY_WEBSITES, PROCRASTINATION_WEBSITES, PROCRASTINATION_APPS,
    LOG_FILE, LOG_LEVEL, IB_QUOTES
)


class StudyTimer:
    """Main tracking daemon with project name extraction"""

    def __init__(self):
        # Initialize trackers
        try:
            from trackers.app_tracker import AppTracker as RealAppTracker
            from trackers.browser_tracker import BrowserTracker as RealBrowserTracker
            from trackers.file_tracker import FileTracker as RealFileTracker
            self.app_tracker = RealAppTracker()
            self.browser_tracker = RealBrowserTracker()
            self.file_tracker = RealFileTracker()
            self.use_mock = False
        except ImportError:
            print("⚠️  Real trackers not available, using mock trackers for testing")
            from trackers.mock_tracker import AppTracker, BrowserTracker, FileTracker
            self.app_tracker = AppTracker()
            self.browser_tracker = BrowserTracker()
            self.file_tracker = FileTracker()
            self.use_mock = True

        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()
        self.current_session = None
        self.session_start = None
        self.last_activity_time = None
        self.session_break_threshold = 900  # 15 minutes
        self.current_session_is_study = False
        self.current_session_is_procrastination = False

        # Initialize project extractor
        try:
            from trackers.project_extractor import extract_project_name
            self.extract_project_name = extract_project_name
        except ImportError:
            # Fallback function
            def extract_project_name(url, page_title=None):
                if url:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    return parsed.netloc.replace('www.', '').split('.')[0].title()
                return None
            self.extract_project_name = extract_project_name

        self.setup_logging()
        self.logger.info("Study Timer initialized with PROJECT NAME TRACKING!")

    def is_system_asleep(self):
        """Check if system is asleep or screen is locked"""
        try:
            # Try to use real system detection first
            if not self.use_mock:
                return self._is_system_really_asleep()
            else:
                # Mock implementation - use mock tracker's sleep state
                return not self.app_tracker.is_system_awake()
        except:
            # Fallback to mock if real detection fails
            return False

    def _is_system_really_asleep(self):
        """Real system sleep detection using macOS APIs"""
        try:
            from AppKit import NSWorkspace
            workspace = NSWorkspace.sharedWorkspace()

            # Check if screen is locked by trying to get active application
            # If we can't get it, screen might be locked
            try:
                active_app = workspace.activeApplication()
                if not active_app or not active_app.get('NSApplicationName'):
                    return True
            except:
                return True

            # Additional check: see if we can access the frontmost application
            try:
                front_app = workspace.frontmostApplication()
                if not front_app:
                    return True
            except:
                return True

            return False

        except ImportError:
            # If macOS APIs not available, assume not asleep
            return False

    def wait_for_system_wake(self):
        """Wait for system to wake up from sleep/lock"""
        self.logger.info("💤 System appears to be asleep or locked, pausing tracking...")

        while self.is_system_asleep():
            if self.use_mock:
                # For mock, just wait a bit and check again
                time.sleep(5)
            else:
                # For real system, check every 10 seconds
                time.sleep(10)

        self.logger.info("✅ System is awake, resuming tracking!")
    
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
        if app_name in PROCRASTINATION_APPS:
            self.logger.debug(f"[CLASSIFY] {app_name} is PROCRASTINATION_APP")
            return (False, True)
        
        if app_name in STUDY_APPS:
            self.logger.debug(f"[CLASSIFY] {app_name} is STUDY_APP")
            if self.browser_tracker.is_browser(app_name) and url:
                self.logger.debug(f"[CLASSIFY] {app_name} is a browser, checking URL: {url}")
                category = self.browser_tracker.categorize_website(
                    url, STUDY_WEBSITES, PROCRASTINATION_WEBSITES
                )
                self.logger.debug(f"[CLASSIFY] URL category: {category}")
                if category == 'study':
                    return (True, False)
                elif category == 'procrastination':
                    return (False, True)
                return (False, False)
            self.logger.debug(f"[CLASSIFY] {app_name} is study app (non-browser)")
            return (True, False)
        self.logger.debug(f"[CLASSIFY] {app_name} is NOT tracked")
        return (False, False)
    
    def should_start_new_session(self):
        """Determine if we should start a new session"""
        if not self.last_activity_time:
            return True
        
        time_since_activity = (datetime.now() - self.last_activity_time).total_seconds()
        return time_since_activity > self.session_break_threshold
    
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
        """Start tracking session WITH PROJECT NAME"""
        try:
            # ✅ EXTRACT PROJECT NAME HERE
            project_name = None
            if activity_data.get('url'):
                project_name = self.extract_project_name(
                    activity_data['url'],
                    activity_data.get('window_title')
                )
                self.logger.info(f"📋 PROJECT DETECTED: {project_name}")
            
            self.cursor.execute("""
                INSERT INTO sessions 
                (app_name, window_title, file_path, website_url, project_name, start_time, is_study, is_procrastination)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                activity_data['app_name'],
                activity_data.get('window_title'),
                activity_data.get('file_path'),
                activity_data.get('url'),
                project_name,  # ✅ NEW!
                activity_data['timestamp'],
                is_study,
                is_procrastination
            ))
            self.conn.commit()
            self.current_session = self.cursor.lastrowid
            self.session_start = activity_data['timestamp']
            self.current_session_is_study = is_study
            self.current_session_is_procrastination = is_procrastination
            
            status = "STUDYING" if is_study else "PROCRASTINATING" if is_procrastination else "WORKING"
            project_info = f" | Project: {project_name}" if project_name else ""
            self.logger.info(f"New session: {status} - {activity_data['app_name']}{project_info}")
        except Exception as e:
            self.logger.error(f"Error starting session: {e}")
    
    def update_session(self, activity_data):
        """Update the current session with new activity data AND PROJECT NAME"""
        if not self.current_session:
            return
        
        try:
            # ✅ EXTRACT PROJECT NAME FOR UPDATES TOO
            project_name = None
            if activity_data.get('url'):
                project_name = self.extract_project_name(
                    activity_data['url'],
                    activity_data.get('window_title')
                )
            
            self.cursor.execute("""
                UPDATE sessions 
                SET end_time = ?,
                    duration = ?,
                    app_name = ?,
                    window_title = ?,
                    file_path = ?,
                    website_url = ?,
                    project_name = ?
                WHERE id = ?
            """, (
                activity_data['timestamp'],
                int((activity_data['timestamp'] - self.session_start).total_seconds()),
                activity_data['app_name'],
                activity_data.get('window_title'),
                activity_data.get('file_path'),
                activity_data.get('url'),
                project_name,  # ✅ NEW!
                self.current_session
            ))
            self.conn.commit()
            self.logger.debug(f"[SESSION UPDATE] Session {self.current_session}: {activity_data['app_name']} | URL: {activity_data.get('url', 'N/A')} | Project: {project_name}")
        except Exception as e:
            self.logger.error(f"Error updating session: {e}")
    
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
            self.logger.info(f"Session ended: {duration}s ({duration//60}m)")
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

    def is_tab_active(self):
        """Check if the dashboard tab is currently active"""
        try:
            # Check the most recent tab activity status from the database
            self.cursor.execute("""
                SELECT is_active, timestamp
                FROM tab_activity
                ORDER BY timestamp DESC
                LIMIT 1
            """)

            result = self.cursor.fetchone()
            if result and result['is_active']:
                return True
            elif result is None:
                # If no tab activity data yet, assume active (for backwards compatibility)
                return True
            else:
                return False
        except Exception as e:
            self.logger.debug(f"Error checking tab activity: {e}")
            # If we can't check, assume active to avoid breaking tracking
            return True

    def run(self):
        """Main loop"""
        self.logger.info("🚀 Starting study tracking with PROJECT NAME extraction...")
        self.logger.info("Session break threshold: 15 minutes")
        self.logger.info("✅ Kognity will be tracked!")
        self.logger.info("✅ Project names will be extracted automatically!")
        self.logger.info("✅ Real sleep/lock detection enabled")
        self.logger.info("✅ Tab activity tracking enabled")
        update_counter = 0

        try:
            while True:
                # Check if system is asleep or locked
                if self.is_system_asleep():
                    self.wait_for_system_wake()
                    continue

                # Check if dashboard tab is active
                if not self.is_tab_active():
                    self.logger.debug("📱 Dashboard tab is inactive, pausing tracking...")
                    # If we have an active session, pause it until tab becomes active
                    if self.current_session:
                        self.logger.info("📱 Tab became inactive, pausing current session")
                        # Note: We don't end the session, just pause tracking until tab is active again
                    time.sleep(TRACKING_INTERVAL)
                    continue

                # If tab just became active and we had a paused session, resume it
                if self.current_session:
                    self.logger.debug("📱 Dashboard tab is active, resuming tracking")
                else:
                    self.logger.debug("📱 Dashboard tab is active, ready to track new sessions")

                activity = self.app_tracker.get_current_activity()
                app_name = activity['app_name']
                current_time = datetime.now()
                
                # Check if user is idle
                if self.app_tracker.is_idle(IDLE_TIMEOUT):
                    if self.last_activity_time:
                        time_since_activity = (current_time - self.last_activity_time).total_seconds()
                        if time_since_activity > self.session_break_threshold:
                            # Check if system might be asleep (long idle time)
                            if self.is_system_asleep():
                                self.logger.info("💤 System went to sleep during idle period, pausing...")
                                self.wait_for_system_wake()
                                continue
                            else:
                                if self.current_session:
                                    self.logger.info("15+ minutes of inactivity, ending session")
                                    self.end_current_session(self.last_activity_time)
                                    self.last_activity_time = None

                    time.sleep(TRACKING_INTERVAL)
                    continue
                
                # User is active
                self.last_activity_time = current_time
                
                # Get browser activity if applicable
                url = None
                if self.browser_tracker.is_browser(app_name):
                    browser_activity = self.browser_tracker.get_browser_activity(app_name)
                    url = browser_activity.get('url')
                
                is_study, is_procrastination = self.is_study_activity(app_name, url)
                
                # Build activity data
                activity_data = {
                    'timestamp': activity['timestamp'],
                    'app_name': app_name,
                    'window_title': activity['window_title'],
                    'file_path': activity['file_path'],
                    'url': url
                }
                
                # DEBUG: Log all activity detection
                self.logger.debug(f"[ACTIVITY] App: {app_name} | URL: {url} | Study: {is_study} | Procrastination: {is_procrastination}")
                
                # Log activity
                self.log_activity(activity_data)
                
                # Handle session tracking
                if is_study or is_procrastination:
                    if not self.current_session:
                        self.logger.debug(f"[SESSION] No active session, starting new one")
                        self.start_new_session(activity_data, is_study, is_procrastination)
                    elif self.should_start_new_session():
                        self.logger.info("15+ minute break detected, starting new session")
                        self.end_current_session(self.last_activity_time)
                        self.start_new_session(activity_data, is_study, is_procrastination)
                    elif (is_study != self.current_session_is_study or
                          is_procrastination != self.current_session_is_procrastination):
                        self.logger.info(f"Activity type changed, starting new session")
                        self.end_current_session(self.last_activity_time)
                        self.start_new_session(activity_data, is_study, is_procrastination)
                    else:
                        self.logger.debug(f"[SESSION] Continuing session {self.current_session}")
                        self.update_session(activity_data)
                        self.current_session_is_study = is_study
                        self.current_session_is_procrastination = is_procrastination
                else:
                    self.logger.debug(f"[ACTIVITY] Not tracked: {app_name}")
                
                # Update daily stats every 10 iterations
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
    print("STUDYTIME - Academic Time Tracker v2.1")
    print("=" * 60)
    print("\n✅ NEW FEATURES:")
    print("   • Automatic PROJECT NAME extraction")
    print("   • Kognity course tracking (IB Chemistry, etc.)")
    print("   • GitHub repo tracking")
    print("   • Google Docs/Slides/Sheets document names")
    print("   • Sleep/lock detection (no tracking when away)")
    print("   • Tab activity tracking (only tracks when dashboard is active)")
    print("   • And more!")
    print("\nGrant Accessibility permissions in System Preferences!")
    print("   (Security & Privacy → Privacy → Accessibility)\n")
    
    timer = StudyTimer()
    timer.run()


if __name__ == "__main__":
    main()
