# StudyTime - Quick Reference

## 🚀 Quick Start

```bash
# Setup (first time only)
chmod +x start.sh
./start.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/init_db.py
```

## 🎯 Running the Application

### 🔥 One-Command Start (NEW!)
```bash
# Start everything in one terminal!
cd ~/Documents/GitHub/Study-Timer
./run.sh

# This automatically:
# 1. Kills existing processes
# 2. Starts tracker in background
# 3. Starts dashboard at http://localhost:5000
# 4. Shows debug logs
```

### Terminal 1: Start the Tracker
```bash
cd ~/Documents/GitHub/Study-Timer
source venv/bin/activate
python src/main.py
```

### Terminal 2: Start the Dashboard
```bash
cd ~/Documents/GitHub/Study-Timer
source venv/bin/activate
python src/dashboard/app.py
```

Then open http://localhost:5000 in your browser!

## 🔧 Configuration

Edit `src/config.py` to customize:
- **TRACKING_INTERVAL**: How often to check activity (default: 5 seconds)
- **IDLE_TIMEOUT**: Inactivity threshold (default: 300 seconds)
- **STUDY_APPS**: Apps to track (add your study apps!)
- **STUDY_WEBSITES**: Websites considered "study" time
- **PROCRASTINATION_WEBSITES**: Websites that... aren't studying 😅

## 📊 What Gets Tracked?

✅ **Applications**: Any app in your STUDY_APPS list  
✅ **Files**: Document names you're working on  
✅ **Websites**: URLs in Chrome, Safari, Firefox  
✅ **Time**: Duration of each session  
✅ **Categories**: Study vs. Procrastination  

## 🎨 IB Student Features

The dashboard includes:
- **Daily study time** with motivational IB quotes
- **Weekly charts** to see your study patterns
- **App breakdowns** showing where your time goes
- **Recent files** you've worked on
- **Study streak** counter (days in a row!)
- **Procrastination tracking** (we won't judge... much)

## 🔐 Privacy

All data is stored locally in `data/study_data.db`. Nothing is sent to the cloud. Your procrastination secrets are safe with us!

## 🐛 Troubleshooting

### "Permission Denied" Errors
Grant Accessibility permissions:
1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Click the lock to make changes
3. Add Terminal (or iTerm) and Python to the list

### No Data Showing
1. Make sure the tracker (main.py) is running
2. Work in one of your configured STUDY_APPS
3. Wait a few seconds for tracking to start
4. Refresh the dashboard

### Browser URLs Not Tracking
AppleScript needs permission to control your browser:
1. System Preferences → Security & Privacy → Privacy → Automation
2. Allow Terminal/Python to control Chrome/Safari/Firefox

## 📝 Database Schema

The tracker uses SQLite with three main tables:

- **sessions**: Individual study sessions with start/end times
- **activity_log**: Detailed log of every check (every 5 seconds)
- **daily_stats**: Aggregated daily statistics

## 🤝 Contributing

Found a bug? Want a feature? This is a student project, so:
1. Fork it
2. Fix it
3. PR it
4. Profit! (in IB points, not actual money)

## 💡 Tips for IB Students

- **Theory of Knowledge**: Is tracking your study time studying, or procrastinating about studying?
- **Extended Essay**: Track your research sessions! See how much time you *actually* spend on it.
- **CAS Hours**: Sorry, this won't inflate your CAS hours. That would be unethical (and we track procrastination).
- **Study Strategy**: Use the data to identify your most productive times and apps!

---

Made with ☕ and existential dread by an IB student who should be studying right now.
