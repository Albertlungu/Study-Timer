"""
Mock App Tracker for testing (works without macOS frameworks)
"""

import time
from datetime import datetime
import random


class AppTracker:
    """Mock app tracker for testing"""

    def __init__(self):
        self.last_app = None
        self.last_window = None
        self.sleep_start_time = None

    def get_current_activity(self):
        """Get mock current activity"""
        # Simulate different apps
        apps = ["Safari", "Google Chrome", "PyCharm", "Terminal", "Notes", "Finder"]
        current_app = random.choice(apps)

        return {
            'timestamp': datetime.now(),
            'app_name': current_app,
            'window_title': f"Mock Window - {current_app}",
            'file_path': f"/mock/path/to/{current_app.lower()}.txt"
        }

    def get_active_application(self):
        """Get mock active application"""
        apps = ["Safari", "Google Chrome", "PyCharm", "Terminal", "Notes"]
        return random.choice(apps)

    def get_active_window_title(self):
        """Get mock window title"""
        return "Mock Window Title"

    def is_idle(self, timeout):
        """Mock idle check"""
        return False

    def simulate_sleep(self, duration_minutes=30):
        """Simulate system going to sleep"""
        self.sleep_start_time = datetime.now()
        print(f"😴 Mock system going to sleep for {duration_minutes} minutes...")

    def is_system_awake(self):
        """Check if mock system is awake"""
        if self.sleep_start_time:
            sleep_duration = (datetime.now() - self.sleep_start_time).total_seconds()
            if sleep_duration > 1800:  # 30 minutes
                print("✅ Mock system waking up!")
                self.sleep_start_time = None
                return True
            return False
        return True


class BrowserTracker:
    """Mock browser tracker"""

    def __init__(self):
        pass

    def is_browser(self, app_name):
        """Check if app is a browser"""
        browsers = ["Safari", "Google Chrome", "Firefox", "Arc"]
        return app_name in browsers

    def get_browser_activity(self, app_name):
        """Get mock browser activity"""
        return {
            'url': f"https://mock-{app_name.lower()}.com/page",
            'title': f"Mock {app_name} Page"
        }

    def categorize_website(self, url, study_sites, procrastination_sites):
        """Categorize website"""
        if any(site in url for site in study_sites):
            return 'study'
        elif any(site in url for site in procrastination_sites):
            return 'procrastination'
        return 'other'


class FileTracker:
    """Mock file tracker"""

    def __init__(self):
        pass

    def get_current_file(self):
        """Get mock current file"""
        return "/mock/current/file.py"

    def is_text_file(self, filepath):
        """Check if file is a text file"""
        return filepath.endswith(('.py', '.txt', '.md', '.js', '.html', '.css'))
