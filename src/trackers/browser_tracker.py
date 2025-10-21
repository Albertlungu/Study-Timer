"""
Browser Tracker Module

Specialized tracking for web browsers to extract URLs and page titles.
Supports Chrome, Safari, and Firefox.
"""

import subprocess
import re
from urllib.parse import urlparse


class BrowserTracker:
    """Tracks browser activity and extracts URLs"""
    
    def __init__(self):
        self.supported_browsers = ['Google Chrome', 'Safari', 'Firefox']
    
    def is_browser(self, app_name):
        """
        Check if the application is a supported browser
        
        Args:
            app_name (str): Application name
        
        Returns:
            bool: True if app is a supported browser
        """
        return app_name in self.supported_browsers
    
    def get_chrome_url(self):
        """
        Get the current URL from Google Chrome using AppleScript
        
        Returns:
            tuple: (url, page_title) or (None, None) if unavailable
        """
        script = '''
        tell application "Google Chrome"
            if (count of windows) > 0 then
                set currentTab to active tab of front window
                set currentURL to URL of currentTab
                set currentTitle to title of currentTab
                return currentURL & "|SPLIT|" & currentTitle
            end if
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split('|SPLIT|')
                if len(parts) == 2:
                    return parts[0], parts[1]
        except Exception as e:
            print(f"Error getting Chrome URL: {e}")
        
        return None, None
    
    def get_safari_url(self):
        """
        Get the current URL from Safari using AppleScript
        
        Returns:
            tuple: (url, page_title) or (None, None) if unavailable
        """
        script = '''
        tell application "Safari"
            if (count of windows) > 0 then
                set currentURL to URL of current tab of front window
                set currentTitle to name of current tab of front window
                return currentURL & "|SPLIT|" & currentTitle
            end if
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split('|SPLIT|')
                if len(parts) == 2:
                    return parts[0], parts[1]
        except Exception as e:
            print(f"Error getting Safari URL: {e}")
        
        return None, None
    
    def get_firefox_url(self):
        """
        Get the current URL from Firefox (more limited than Chrome/Safari)
        
        Note: Firefox doesn't expose as much via AppleScript,
        so this tries to extract from window title which often contains the URL
        
        Returns:
            tuple: (url, page_title) or (None, None) if unavailable
        """
        # Firefox is trickier; we can get the window title but not always the URL
        # The window title format is usually: "Page Title - Mozilla Firefox"
        # For now, we'll return None and rely on window title tracking
        return None, None
    
    def get_browser_activity(self, app_name):
        """
        Get current URL and page title from active browser
        
        Args:
            app_name (str): Name of the browser application
        
        Returns:
            dict: Contains 'url' and 'page_title', or both None if unavailable
        """
        url, page_title = None, None
        
        if app_name == "Google Chrome":
            url, page_title = self.get_chrome_url()
        elif app_name == "Safari":
            url, page_title = self.get_safari_url()
        elif app_name == "Firefox":
            url, page_title = self.get_firefox_url()
        
        return {
            'url': url,
            'page_title': page_title,
            'domain': self.extract_domain(url) if url else None
        }
    
    def extract_domain(self, url):
        """
        Extract the domain from a URL
        
        Args:
            url (str): Full URL
        
        Returns:
            str: Domain name (e.g., 'docs.google.com')
        """
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return None
    
    def categorize_website(self, url, study_domains, procrastination_domains):
        """
        Categorize a website as study or procrastination
        
        Args:
            url (str): Website URL
            study_domains (list): List of study-related domains
            procrastination_domains (list): List of procrastination domains
        
        Returns:
            str: 'study', 'procrastination', or 'unknown'
        """
        if not url:
            return 'unknown'
        
        domain = self.extract_domain(url)
        if not domain:
            return 'unknown'
        
        # Check if domain matches any study sites
        for study_domain in study_domains:
            if study_domain in domain:
                return 'study'
        
        # Check if domain matches any procrastination sites
        for proc_domain in procrastination_domains:
            if proc_domain in domain:
                return 'procrastination'
        
        return 'unknown'


# Test function
if __name__ == "__main__":
    print("🌐 Testing Browser Tracker...")
    print("Make sure Chrome or Safari is open with an active tab!\n")
    
    import time
    from sys import path
    from pathlib import Path
    path.append(str(Path(__file__).parent.parent))
    from config import STUDY_WEBSITES, PROCRASTINATION_WEBSITES
    
    tracker = BrowserTracker()
    
    for browser in ['Google Chrome', 'Safari']:
        print(f"Testing {browser}...")
        if tracker.is_browser(browser):
            activity = tracker.get_browser_activity(browser)
            print(f"  URL: {activity['url']}")
            print(f"  Title: {activity['page_title']}")
            print(f"  Domain: {activity['domain']}")
            
            if activity['url']:
                category = tracker.categorize_website(
                    activity['url'],
                    STUDY_WEBSITES,
                    PROCRASTINATION_WEBSITES
                )
                print(f"  Category: {category}")
        print()
        time.sleep(1)
    
    print("✅ Test complete!")
