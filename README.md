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

## Testing

After setup, test the dashboard functionality:

```bash
# Run comprehensive tests
python3 test_dashboard.py

# This will:
# 1. Check database connectivity
# 2. Test all API endpoints
# 3. Add sample data if needed
# 4. Verify chart data availability
```

## Usage

### Start Everything (Recommended)
```bash
./run.sh
```

### Manual Start
```bash
# Terminal 1 - Start the tracker
python3 src/main.py

# Terminal 2 - Start the dashboard
python3 src/dashboard/app.py

# Visit http://localhost:5000
```

### Dashboard Features

- **Modern UI**: Clean, Hackatime-inspired design with dark theme
- **Interactive Charts**: 4 data visualizations with real-time updates
- **Responsive**: Works on desktop, tablet, and mobile
- **Real-time**: Auto-refreshes every 60 seconds
- **Privacy-first**: All data stored locally

#### Charts Available
- **Study Apps Breakdown**: Pie chart of application usage
- **Study Websites Breakdown**: Pie chart of website activity
- **Website Time Distribution**: Bar chart of time spent per site
- **Project Time Tracking**: Bar chart of project-based time analysis

#### Smart Project Detection
Automatically detects projects from URLs:
- **GitHub**: `username/repository` format
- **Google Workspace**: Docs, Sheets, Slides
- **Notion**: Workspace detection
- **Replit**: Project names
- **CodePen**: User/project format
- **VS Code Web**: Online editor detection

## Troubleshooting

**Dashboard not loading?**
```bash
# Test all components
python3 test_dashboard.py
```

**No data showing?**
- Ensure the tracker is running (`python3 src/main.py`)
- Check that accessibility permissions are granted
- Verify database exists in `data/study_data.db`

**Charts not rendering?**
- Clear browser cache and refresh
- Check browser console for JavaScript errors
- Ensure Chart.js library is loading correctly

## Contributing

Found a bug? Want to add a feature? PRs welcome! This is a student project, so code quality ranges from "pretty good" to "written at 2 AM before a deadline."

## License

MIT License - because sharing is caring, and we're all in this together.

---
