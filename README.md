# 📚 Study Timer - Your Personal Procrastination Detector

*Because CAS hours don't track themselves, but this app tracks your actual study time.*

## What is this?

Study Timer is a macOS background application that automatically tracks your study sessions by monitoring:
- **Applications**: Obsidian, Apple Notes, Google Docs, Google Slides, VS Code, etc.
- **Specific Files**: Tracks which documents you're working on
- **Websites**: Monitors study-related websites in your browser
- **Time Analytics**: Shows you where your study time actually goes (spoiler: Reddit doesn't count)

Inspired by Wakatime and Hackatime, but designed specifically for students who need to track their study habits without manually starting timers.

## Features

✨ **Automatic Tracking**: Runs silently in the background  
📊 **Beautiful Dashboard**: View your stats in a web interface  
📝 **Document-Level Tracking**: See which specific files you worked on  
🎨 **IB-Themed Humor**: Because if you don't laugh, you'll cry  
🔒 **Privacy First**: All data stored locally on your machine  
⚡ **Lightweight**: Minimal CPU and memory usage  

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
   - This allows the app to read window titles and track your activity

5. **Initialize the database**
```bash
python src/init_db.py
```

## Usage

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
Study-Timer/
├── README.md                 # You are here!
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

**Q: Will this help me pass my IB exams?**  
A: It'll help you realize how much time you *don't* spend studying. The rest is up to you. 😅

## IB Student Special Features

- **Theory of Knowledge Mode**: Tracks time spent contemplating the nature of procrastination
- **CAS Hour Calculator**: See if your "Extended Essay research" counts as Creativity, Activity, or Service (spoiler: it's none)
- **Predicted Grade Motivator**: Dashboard shows increasingly desperate messages as deadlines approach

## Contributing

Found a bug? Want to add a feature? PRs welcome! This is a student project, so code quality ranges from "pretty good" to "written at 2 AM before a deadline."

## License

MIT License - because sharing is caring, and we're all in this together.

---

*Made with ☕, 😭, and a concerning amount of caffeine by an IB student who should probably be studying instead of coding this.*
