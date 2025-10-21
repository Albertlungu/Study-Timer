# Changelog

All notable changes to Study Timer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-21

### 🎉 Initial Release

The first complete version of Study Timer - your personal procrastination detector!

### Added

#### Core Tracking System
- **AppTracker**: Monitors active applications and window titles
- **BrowserTracker**: Extracts URLs and page titles from Chrome, Safari, and Firefox
- **FileTracker**: Detects and categorizes files being worked on
- Automatic session tracking with start/end times
- Idle detection (5-minute default timeout)
- Study vs. procrastination categorization

#### Database
- SQLite database with three main tables:
  - `sessions`: Individual study sessions
  - `activity_log`: Detailed activity logging
  - `daily_stats`: Aggregated daily statistics
- Automatic daily statistics calculation
- Session duration tracking

#### Dashboard
- Beautiful web interface with gradient purple theme
- Real-time statistics display with auto-refresh (30s interval)
- **Today's Stats**: Study time, procrastination time, session count
- **Weekly Chart**: Bar chart showing study vs. procrastination over 7 days
- **Top Apps**: Most-used applications this week
- **Recent Files**: Files you've worked on recently
- **Session History**: Last 24 hours of activity
- **Overall Stats**: Total study time, daily average, best day, current streak
- IB-themed motivational quotes that rotate daily

#### Configuration
- Comprehensive config system in `src/config.py`
- Customizable tracking interval (default: 5s)
- Customizable idle timeout (default: 5min)
- Extensive list of study apps (Obsidian, Apple Notes, Google Suite, etc.)
- Predefined study websites (Google Docs, GitHub, Wikipedia, etc.)
- Predefined procrastination websites (YouTube, Reddit, social media, etc.)
- 8 hilarious IB-themed quotes

#### Documentation
- Comprehensive README with features and installation
- QUICKSTART guide for quick reference
- Detailed INSTALL guide with step-by-step instructions
- Troubleshooting section for common issues

#### Scripts
- `start.sh`: Automated setup script
- `test.sh`: Component testing script
- `commit.sh`: Git commit helper
- Database initialization script

### Technical Details
- Built with Python 3.8+
- Flask web framework for dashboard
- Chart.js for beautiful visualizations
- PyObjC for macOS application monitoring
- AppleScript for browser URL extraction
- SQLite for local data storage

### Features for IB Students
- Subject detection from file names (Math, Physics, Chemistry, Biology, etc.)
- Special categories for TOK, Extended Essay, CAS, and IAs
- IB-themed humor throughout the interface
- Study streak tracker (because consistency matters!)
- Procrastination time tracking (for honest self-reflection)

### Privacy & Security
- All data stored locally (no cloud, no tracking, no telemetry)
- No external API calls
- Database stays on your machine
- You own your data completely

### Known Limitations
- macOS only (uses Cocoa/Quartz APIs)
- Requires Accessibility permissions
- Browser URL tracking needs Automation permissions
- Firefox URL extraction is limited compared to Chrome/Safari

### Future Improvements (Maybe)
- [ ] Windows/Linux support
- [ ] More browser support
- [ ] Export data to CSV/JSON
- [ ] Goals and reminders
- [ ] Pomodoro timer integration
- [ ] Mobile app for stats viewing
- [ ] Study efficiency scoring
- [ ] Subject-based analytics

---

## How to Upgrade

When new versions are released:

```bash
cd ~/Documents/GitHub/Study-Timer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

Made with ☕, 😭, and way too much caffeine by an IB student.
