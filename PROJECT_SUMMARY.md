# Study Timer - Project Summary

## 📚 What is This?

Study Timer is a **macOS background application** that automatically tracks your study sessions by monitoring which applications you use, which files you work on, and which websites you visit. Think of it as Wakatime, but for studying instead of coding!

Created by an IB student who needed a better way to track study time without manually starting timers.

## 🎯 Key Features

### Automatic Tracking
- Runs silently in the background
- No manual start/stop required
- Tracks apps, files, and websites
- Smart idle detection

### Beautiful Dashboard
- Real-time web interface
- Weekly charts and analytics
- Study vs. procrastination tracking
- Session history viewer
- IB-themed humor

### Smart Categorization
- Knows what's "studying" vs. "procrastinating"
- Tracks specific documents and files
- Subject detection (Math, Physics, TOK, etc.)
- Browser URL extraction

### Privacy First
- All data stored locally
- No cloud sync
- No external API calls
- You own your data

## 🛠️ Technology Stack

- **Language**: Python 3.8+
- **Web Framework**: Flask
- **Database**: SQLite
- **macOS APIs**: PyObjC (Cocoa, Quartz)
- **Visualization**: Chart.js
- **Automation**: AppleScript (for browsers)

## 📁 Project Structure

```
Study-Timer/
├── src/
│   ├── main.py                 # Main tracking daemon
│   ├── config.py               # Configuration
│   ├── init_db.py              # Database setup
│   ├── trackers/               # Tracking modules
│   │   ├── app_tracker.py      # Application monitoring
│   │   ├── browser_tracker.py  # Browser URL extraction
│   │   └── file_tracker.py     # File detection
│   └── dashboard/              # Web dashboard
│       ├── app.py              # Flask application
│       └── templates/          # HTML templates
├── data/                       # SQLite database (gitignored)
├── logs/                       # Log files (gitignored)
├── docs/                       # Documentation
├── start.sh                    # Setup script
├── test.sh                     # Testing script
├── status.sh                   # Status checker
└── README.md                   # Main documentation
```

## 📊 Database Schema

### sessions
- Individual study sessions
- Start/end times, duration
- App, file, URL information
- Study vs. procrastination flag

### activity_log
- Detailed activity logging
- Every 5-second check recorded
- Full context captured

### daily_stats
- Aggregated daily statistics
- Total study time, sessions
- IB motivational quotes

## 🚀 How It Works

1. **Tracker Loop** (main.py)
   - Runs every 5 seconds
   - Checks active application
   - Gets window title and file info
   - Extracts browser URLs if applicable
   - Logs to database

2. **Session Management**
   - Detects app/file changes
   - Starts new sessions automatically
   - Ends sessions on switch or idle
   - Calculates duration

3. **Dashboard** (Flask)
   - Queries SQLite database
   - Provides REST API endpoints
   - Auto-refreshes every 30 seconds
   - Beautiful visualizations

## 🎓 Perfect for IB Students

### Extended Essay
- Track research time
- Monitor writing sessions
- See total hours invested
- Prove you worked hard!

### Internal Assessments
- Track each IA separately
- Compare time across subjects
- Identify which need more work

### General Studying
- Daily study goals
- Consistency tracking (streaks!)
- Subject time distribution
- Procrastination awareness

### CAS Documentation
- Track creative projects
- Monitor activity time
- (But don't inflate your hours - that's unethical!)

## 🔒 Privacy & Security

- **Local Storage**: Everything in SQLite on your Mac
- **No Telemetry**: Zero data sent anywhere
- **No Accounts**: No login, no cloud
- **Open Source**: Audit the code yourself
- **Gitignore**: Database never committed

## 🎨 Design Philosophy

### For Students, By Students
- Understands IB pain
- Built by someone in the trenches
- Humor to cope with stress
- Actually useful features

### Minimalist but Powerful
- Simple setup
- Runs in background
- Beautiful but not distracting
- Data when you need it

### Privacy Matters
- Your study habits are personal
- No one else needs to know
- Data stays on your machine
- Complete control

## 📈 Stats You Get

- **Today**: Study time, sessions, most-used app
- **This Week**: Daily breakdown with charts
- **All Time**: Total time, averages, best days
- **Streaks**: Consecutive days studied
- **Apps**: Time per application
- **Files**: Documents worked on
- **Sessions**: Complete history

## 🛣️ Future Possibilities

- Windows/Linux support
- More browser support  
- Export features (CSV, JSON)
- Study goals and reminders
- Pomodoro integration
- Mobile app for stats
- Cloud sync (optional)
- AI-powered insights

## 🤝 Contributing

Contributions welcome! See CONTRIBUTING.md for:
- How to report bugs
- How to suggest features
- Development setup
- Coding standards
- Pull request process

## 📝 Documentation Files

- **README.md** - Project overview
- **INSTALL.md** - Detailed installation
- **QUICKSTART.md** - Quick reference
- **FEATURES.md** - Feature showcase
- **CONTRIBUTING.md** - Contribution guide
- **CHANGELOG.md** - Version history
- **LICENSE** - MIT License

## 💪 Why This Matters

### The Problem
- IB students study a LOT
- Hard to track actual time invested
- Easy to overestimate (or underestimate)
- Manual timers are annoying
- Need data to improve habits

### The Solution
- Automatic tracking = no effort
- Honest data = better awareness
- Visualizations = clear insights
- History = see progress
- Privacy = peace of mind

## 🎯 Success Metrics

A successful Study Timer:
- Runs reliably in background
- Accurately captures study sessions
- Provides useful insights
- Respects privacy completely
- Actually helps students
- Makes IB slightly less painful

## 🙏 Acknowledgments

Built with:
- Too much coffee ☕
- Not enough sleep 😴
- A lot of procrastination 😅
- Genuine desire to help 💪

Inspired by:
- Wakatime (for coding)
- RescueTime (for productivity)
- IB stress (for motivation)

## 📜 License

MIT License - Share freely, use widely, study hard!

---

**Made by an IB student who should be studying right now.** 

But hey, at least this tool will help track how much time I waste making it! 😄📚✨
