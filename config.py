"""
Configuration settings for Study Timer

Customize these settings to match your study workflow!
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Database
DATABASE_PATH = DATA_DIR / "study_data.db"

# Tracking settings
TRACKING_INTERVAL = 5  # seconds between checks
IDLE_TIMEOUT = 300  # seconds of inactivity before considering user idle (5 minutes)

# Applications to track (add more as needed!)
STUDY_APPS = [
    "Obsidian",
    "Notes",  # Apple Notes
    "Comet",
    "Arc",
    "Google Chrome",
    "Safari",
    "Firefox",
    "Microsoft Word",
    "Microsoft Excel",
    "Microsoft PowerPoint",
    "Pages",
    "Numbers",
    "Keynote",
    "Preview",
    "Skim",  # PDF reader
    "PyCharm",
    "Xcode",
    "Terminal",
    "iTerm",
    "iTerm2",  # iTerm2 specifically
    "Notion",
    "Bear",
    "Evernote",
    "GoodNotes",
    "Notability",
]

# Study-related websites (these will be tracked when in browsers)
STUDY_WEBSITES = [
    "docs.google.com/document",
    "docs.google.com/presentation",
    "drive.google.com",
    "docs.google.com/spreadsheets",
    "classroom.google.com",
    "overleaf.com",
    "notion.so",
    "github.com",
    "stackoverflow.com",
    "scholar.google.com",
    "wikipedia.org",
    "coursera.org",
    "khanacademy.org",
    "quizlet.com",
    "canvas.instructure.com",
    "moodle",
    "blackboard",
    # IB specific - KOGNITY ADDED HERE!
    "ibdocuments.com",
    "app.kognity.com",  # ✅ Already here!
    "kognity.com",       # ✅ Already here!
    "ibo.org",
    "managebac.com",
]

# Procrastination websites (for fun stats, not blocked!)
PROCRASTINATION_WEBSITES = [
    "youtube.com",
    "reddit.com",
    "twitter.com",
    "instagram.com",
    "tiktok.com",
    "facebook.com",
    "netflix.com",
    "twitch.tv",
    "discord.com",
]

# Procrastination apps
PROCRASTINATION_APPS = [
    "Code",  # VS Code - moved from study apps
]

# Dashboard settings
DASHBOARD_PORT = 5000
DASHBOARD_HOST = "127.0.0.1"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "tracker.log"

# IB Humor settings (because we need to laugh)
IB_QUOTES = [
    "Theory of Knowledge: Is this really studying, or are you just procrastinating philosophically?",
    "CAS Hours: 0. Study Hours: Also approaching 0. Coincidence? 🤔",
    "Extended Essay: The only essay that's truly extended... indefinitely.",
    "Your study time is inversely proportional to your exam proximity.",
    "IB Learner Profile: Balanced? Let's check your study-to-Netflix ratio first.",
    "Remember: 45 points requires slightly more than 45 minutes of study.",
    "Internal Assessments: Because external stress wasn't enough.",
    "Sleep is IB Optional.",
]
