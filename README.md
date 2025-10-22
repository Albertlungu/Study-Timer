# StudyTime - Your Personal Academic Time Tracker

*Because CAS hours don't track themselves, but StudyTime tracks your actual study time.*

## What is this?

StudyTime is a macOS background application that automatically tracks your study sessions by monitoring:
- **Applications**: Obsidian, Apple Notes, Google Docs, Google Slides, VS Code, etc.
- **Specific Files**: Tracks which documents you're working on
- **Websites**: Monitors study-related websites in your browser
- **Time Analytics**: Shows you where your study time actually goes (spoiler: Reddit doesn't count)

Inspired by Wakatime and Hackatime, but designed specifically for students who need to track their study habits without manually starting timers.

## Features

- **Automatic Tracking**: Runs silently in the background
- **Modern Dashboard**: Clean, dark mode design with real-time stats and interactive charts
- **Document-Level Tracking**: See which specific files you worked on
- **Data Visualization**: Pie charts and bar graphs showing app usage, website time, and project tracking
- **Cross-App Sessions**: Sessions continue when switching between study applications
- **Privacy First**: All data stored locally on your machine
- **Lightweight**: Minimal CPU and memory usage

## Installation

### Prerequisites
- macOS 10.15 or later
- Python 3.8+
- Homebrew (recommended)

### Setup

1. **Clone the repository**
```bash
cd ~/Documents/GitHub
git clone <your-repo-url> Study-Timer
cd Study-Timer
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Grant Accessibility Permissions**
   - Go to System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Terminal or your Python executable to the list
   - This allows the StudyTime app to read window titles and track your activity

5. **Initialize the database**
```bash
python src/init_db.py
```

## Quick Start

```bash
# One command to start everything!
./run.sh

# This will:
# 1. Kill any existing processes
# 2. Start the tracker in background
# 3. Start the dashboard at http://localhost:5000
# 4. Show you logs for debugging
```

### Start the Tracker
```bash
# Run the tracker daemon
python src/main.py
```

### View Your Dashboard
```bash
# Start the web dashboard (in a new terminal)
python src/dashboard/app.py
```

Then open your browser to `http://localhost:5000`

### Run as Background Service (Optional)
```bash
# Make the tracker start automatically on login
./scripts/install_daemon.sh
```

## Project Structure

```
StudyTime/
├── README.md                 # You are here!
├── run.sh                    # 🚀 One-command startup (NEW!)
├── requirements.txt          # Python dependencies
├── src/
│   ├── main.py              # Main tracking daemon
│   ├── init_db.py           # Database initialization
│   ├── config.py            # Configuration settings
│   ├── trackers/
│   │   ├── __init__.py
│   │   ├── app_tracker.py   # Application tracking logic
│   │   ├── browser_tracker.py # Browser-specific tracking
│   │   └── file_tracker.py  # Document/file tracking
│   └── dashboard/
│       ├── app.py           # Flask web dashboard
│       ├── templates/       # HTML templates
│       └── static/          # CSS, JS, images
├── data/
│   └── study_data.db        # SQLite database (created on init)
└── logs/
    └── tracker.log          # Application logs
```

## Configuration

Edit `src/config.py` to customize:
- Tracking interval (default: 5 seconds)
- Apps to track
- Websites to monitor
- Idle timeout duration

## FAQ

**Q: Will this slow down my Mac?**  
A: Nope! It uses minimal resources and runs with low priority.

**Q: Can I track websites in Chrome/Safari/Firefox?**  
A: Yes! It detects active tabs in all major browsers.

**Q: Does this track me 24/7?**  
A: It only tracks when you're actively using study-related apps. Idle time is detected automatically.

**Q: Where is my data stored?**  
A: Everything is stored locally in `data/study_data.db`. Nothing is sent to the cloud.

## Dashboard Visualizations

StudyTime includes interactive charts that help you understand your study patterns:

- **Study Apps Breakdown**: Pie chart showing which applications you use most for studying
- **Study Websites Breakdown**: Pie chart of your most visited study websites
- **Website Time Distribution**: Bar chart showing time spent on each website
- **Project Time Tracking**: Bar chart analyzing which projects you spend the most time on

The dashboard intelligently detects projects from URLs (GitHub repositories, Google Docs, Notion workspaces, etc.) and tracks time spent on each project across all your study sessions.

## Contributing

Found a bug? Want to add a feature? PRs welcome! This is a student project, so code quality ranges from "pretty good" to "written at 2 AM before a deadline."

## License

MIT License - because sharing is caring, and we're all in this together.

---

*Made with ☕, 😭, and a concerning amount of caffeine by an IB student who should probably be studying instead of coding this.*
