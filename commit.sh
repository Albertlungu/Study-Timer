#!/bin/bash
# Git commit and push script

cd ~/Documents/GitHub/Study-Timer

echo "🔧 Making scripts executable..."
chmod +x start.sh test.sh commit.sh make_executable.sh

echo ""
echo "📦 Adding all files to git..."
git add .

echo ""
echo "💾 Committing changes..."
git commit -m "feat: Complete Study Timer v1.0.0 - Full featured study tracking app

✨ Major Features:
- Automatic tracking of apps, files, and websites
- Beautiful web dashboard with real-time stats
- Study vs procrastination categorization
- Weekly charts and analytics
- File-level tracking (knows what documents you work on)
- Browser URL extraction for Chrome, Safari, Firefox
- IB-themed humor throughout
- Study streak counter
- Session history viewer

📊 Dashboard Includes:
- Today's study time and sessions
- Weekly bar charts with Chart.js
- Top apps usage this week
- Recent files worked on
- Last 24h session timeline
- Overall statistics (total time, averages, best day)
- Auto-refresh every 30 seconds

📝 Documentation:
- Comprehensive README.md
- Detailed INSTALL.md guide
- Quick reference QUICKSTART.md
- Feature showcase in FEATURES.md
- Complete CHANGELOG.md
- MIT LICENSE

🛠️ Scripts & Tools:
- start.sh for automated setup
- test.sh for component testing  
- Database initialization
- Git helper scripts

🔒 Privacy & Security:
- All data stored locally in SQLite
- No cloud sync or external APIs
- Full data ownership
- .gitignore prevents db commits

🎓 Perfect for IB Students:
- Tracks Extended Essay work
- Monitors IA progress
- Subject categorization
- TOK/CAS detection
- Study streak motivation

Built with: Python, Flask, Chart.js, PyObjC, SQLite
Platform: macOS 10.15+
License: MIT"

echo ""
echo "✅ Committed successfully!"
echo ""
echo "📊 Commit summary:"
git log --oneline -1 --stat
echo ""
echo "🚀 Ready to push! Run:"
echo "   git push origin main"
echo ""
echo "   Or if this is your first push:"
echo "   git remote add origin <your-repo-url>"
echo "   git branch -M main"
echo "   git push -u origin main"
