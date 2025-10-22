"""
App Tracker Module

Monitors active applications and their windows on macOS.
Uses Cocoa/Quartz APIs to get window information.
"""

import os
import time
from datetime import datetime
from Quartz import (
    CGWindowListCopyWindowInfo,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID
)
from AppKit import NSWorkspace


class AppTracker:
    """Tracks active applications and their windows"""
    
    def __init__(self):
        self.workspace = NSWorkspace.sharedWorkspace()
        self.last_app = None
        self.last_window = None
        self.last_active_time = None
    
    def get_active_application(self):
        """
        Get the currently active application name
        
        Returns:
            str: Name of the active application
        """
        try:
            active_app = self.workspace.activeApplication()
            return active_app.get('NSApplicationName', 'Unknown')
        except Exception as e:
            print(f"Error getting active app: {e}")
            return None
    
    def get_active_window_title(self):
        """
        Get the title of the currently active window
        
        Returns:
            str: Title of the active window, or None if unavailable
        """
        try:
            # Get list of all on-screen windows
            window_list = CGWindowListCopyWindowInfo(
                kCGWindowListOptionOnScreenOnly,
                kCGNullWindowID
            )
            
            # Find the frontmost window (layer 0)
            for window in window_list:
                if window.get('kCGWindowLayer', 1) == 0:
                    title = window.get('kCGWindowName', '')
                    owner = window.get('kCGWindowOwnerName', '')
                    
                    # Return title if it exists and matches active app
                    if title and owner == self.get_active_application():
                        return title
            
            return None
        except Exception as e:
            print(f"Error getting window title: {e}")
            return None
    
    def extract_file_path(self, window_title, app_name):
        """
        Try to extract file path or document name from window title
        
        Args:
            window_title (str): The window title
            app_name (str): The application name
        
        Returns:
            str: Extracted file path or None
        """
        if not window_title:
            return None
        
        # Common patterns for file paths in window titles
        # Example: "Chapter1.md - Obsidian"
        # Example: "MyDocument.docx - Microsoft Word"
        
        # Split by common separators
        separators = [' - ', ' — ', ' – ', ' | ']
        for sep in separators:
            if sep in window_title:
                parts = window_title.split(sep)
                # Usually the file name is the first part
                potential_file = parts[0].strip()
                
                # Check if it looks like a file (has an extension)
                if '.' in potential_file:
                    return potential_file
        
        # For Apple Notes, the title IS the note name
        if app_name == "Notes":
            return window_title
        
        # For Obsidian, often the window title is just the note name
        if app_name == "Obsidian" and window_title != "Obsidian":
            return window_title
        
        return None
    
    def get_current_activity(self):
        """
        Get comprehensive information about current activity
        
        Returns:
            dict: Activity information containing:
                - app_name: Name of active application
                - window_title: Title of active window
                - file_path: Extracted file/document name
                - timestamp: Current timestamp
                - is_new_session: Whether this is a new session (app/window changed)
        """
        app_name = self.get_active_application()
        window_title = self.get_active_window_title()
        file_path = self.extract_file_path(window_title, app_name)
        current_time = datetime.now()
        
        # Check if this is a new session (different app or window)
        is_new_session = (
            app_name != self.last_app or 
            window_title != self.last_window
        )
        
        # Update tracking state
        self.last_app = app_name
        self.last_window = window_title
        self.last_active_time = current_time
        
        return {
            'app_name': app_name,
            'window_title': window_title,
            'file_path': file_path,
            'timestamp': current_time,
            'is_new_session': is_new_session
        }
    
    def is_idle(self, idle_threshold=300):
        """
        Check if user has been idle for too long
        
        Args:
            idle_threshold (int): Seconds of inactivity to consider idle
        
        Returns:
            bool: True if user is idle
        """
        if not self.last_active_time:
            return False
        
        time_since_active = (datetime.now() - self.last_active_time).total_seconds()
        return time_since_active > idle_threshold


# Test function
if __name__ == "__main__":
    print("🔍 Testing App Tracker...")
    print("Monitoring active window for 30 seconds...\n")
    
    tracker = AppTracker()
    
    for i in range(6):
        activity = tracker.get_current_activity()
        print(f"⏰ Check #{i+1}")
        print(f"  App: {activity['app_name']}")
        print(f"  Window: {activity['window_title']}")
        print(f"  File: {activity['file_path']}")
        print(f"  New Session: {activity['is_new_session']}")
        print()
        
        time.sleep(5)
    
    print("Test complete!")
