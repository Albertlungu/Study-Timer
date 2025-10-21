# Installation & Setup Guide

## Prerequisites

Before you begin, ensure you have:
- **macOS 10.15+** (Catalina or later)
- **Python 3.8+** installed
- **Homebrew** (optional but recommended)
- **Git** for version control

## Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
cd ~/Documents/GitHub
# If you cloned from GitHub:
git clone <your-repo-url> Study-Timer

# Or if you created it locally, it's already here!
cd Study-Timer
```

### 2. Quick Setup (Recommended)

Run the automated setup script:

```bash
chmod +x start.sh
./start.sh
```

This script will:
- Create a Python virtual environment
- Install all dependencies
- Initialize the database
- Provide next steps

### 3. Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Initialize database
python src/init_db.py
```

### 4. Grant System Permissions (IMPORTANT!)

The tracker needs special permissions to monitor your activity:

#### Accessibility Permissions
1. Open **System Preferences** → **Security & Privacy** → **Privacy**
2. Click **Accessibility** in the left sidebar
3. Click the lock icon and enter your password
4. Click **+** and add:
   - Terminal (or iTerm if you use it)
   - Python (usually at `/usr/local/bin/python3` or `/usr/bin/python3`)

#### Automation Permissions (for browser tracking)
1. In **System Preferences** → **Security & Privacy** → **Privacy**
2. Click **Automation** in the left sidebar
3. Check the boxes to allow Terminal/Python to control:
   - Google Chrome
   - Safari
   - Firefox

### 5. Verify Installation

Test that everything works:

```bash
# Make test script executable
chmod +x test.sh

# Run component tests
./test.sh
```

## First Run

### Start the Tracker

In your first terminal:

```bash
cd ~/Documents/GitHub/Study-Timer
source venv/bin/activate
python src/main.py
```

You should see output like:
```
📚 STUDY TIMER - Procrastination Detector 3000
🎯 Mission: Track your study time automatically
⏰ Starting study tracking...
```

### Start the Dashboard

In a second terminal:

```bash
cd ~/Documents/GitHub/Study-Timer
source venv/bin/activate
python src/dashboard/app.py
```

Then open your browser to: **http://localhost:5000**

## Configuration

### Adding More Apps to Track

Edit `src/config.py` and add to the `STUDY_APPS` list:

```python
STUDY_APPS = [
    "Obsidian",
    "Notes",
    "Your App Here",  # Add your apps!
    # ... more apps
]
```

### Adding Study Websites

Add websites to the `STUDY_WEBSITES` list:

```python
STUDY_WEBSITES = [
    "docs.google.com",
    "your-uni-website.edu",  # Add your sites!
    # ... more sites
]
```

### Adjusting Tracking Interval

Change how often the tracker checks your activity (default is 5 seconds):

```python
TRACKING_INTERVAL = 5  # seconds
```

### Adjusting Idle Timeout

Change how long before you're considered "idle" (default is 5 minutes):

```python
IDLE_TIMEOUT = 300  # seconds (5 minutes)
```

## Running as a Background Service (Optional)

To have Study Timer start automatically when you log in:

### Using launchd (macOS)

Create a launch agent file:

```bash
nano ~/Library/LaunchAgents/com.studytimer.tracker.plist
```

Add this content (adjust paths as needed):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.studytimer.tracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USERNAME/Documents/GitHub/Study-Timer/venv/bin/python</string>
        <string>/Users/YOUR_USERNAME/Documents/GitHub/Study-Timer/src/main.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.studytimer.tracker.plist
```

## Troubleshooting

### "Permission Denied" when running scripts

Make them executable:

```bash
chmod +x start.sh test.sh commit.sh
```

### "Module not found" errors

Make sure you've activated the virtual environment:

```bash
source venv/bin/activate
```

### No data appears in dashboard

1. Verify the tracker is running (`python src/main.py`)
2. Make sure you're using a tracked app (check `STUDY_APPS` in config.py)
3. Wait 5-10 seconds for first data to appear
4. Refresh the dashboard

### Browser URLs not being tracked

1. Grant Automation permissions (see Step 4 above)
2. Restart the tracker after granting permissions
3. Make sure you're using Chrome, Safari, or Firefox

### Database errors

If you get database errors, try reinitializing:

```bash
rm data/study_data.db
python src/init_db.py
```

### High CPU usage

Increase the `TRACKING_INTERVAL` in `src/config.py`:

```python
TRACKING_INTERVAL = 10  # Check every 10 seconds instead of 5
```

## Updating

To update Study Timer with new changes:

```bash
cd ~/Documents/GitHub/Study-Timer
git pull origin main
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Uninstallation

To completely remove Study Timer:

```bash
# Stop any running processes
# Then remove the directory
rm -rf ~/Documents/GitHub/Study-Timer

# If you set up launchd:
launchctl unload ~/Library/LaunchAgents/com.studytimer.tracker.plist
rm ~/Library/LaunchAgents/com.studytimer.tracker.plist
```

## Getting Help

- Check the [README.md](README.md) for general information
- See [QUICKSTART.md](QUICKSTART.md) for quick reference
- File issues on GitHub
- Or just debug it yourself - you're an IB student, you got this! 💪

---

Happy tracking! May your study time be high and your procrastination time be low! 📚✨
