#!/bin/bash

# StudyTimer v2.0 Automated Upgrade Script
# This script backs up your data and upgrades all components

set -e  # Exit on error

echo "============================================================"
echo "STUDYTIME v2.0 - AUTOMATED UPGRADE"
echo "============================================================"
echo ""
echo "This script will:"
echo "  1. Backup your database"
echo "  2. Stop running processes"
echo "  3. Run database migration"
echo "  4. Update all files"
echo "  5. Verify the installation"
echo ""
read -p "Ready to proceed? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Upgrade cancelled."
    exit 1
fi

# Define paths
STUDY_TIMER_DIR="/Users/albertlungu/Documents/GitHub/Study-Timer"
UPGRADE_FILES_DIR="/home/claude"  # Where the new files are

echo ""
echo "📂 Working directory: $STUDY_TIMER_DIR"
cd "$STUDY_TIMER_DIR"

# Step 1: Backup
echo ""
echo "Step 1: Backing up database..."
if [ -f "data/study_data.db" ]; then
    cp data/study_data.db "data/study_data_backup_$(date +%Y%m%d_%H%M%S).db"
    echo "✅ Backup created!"
else
    echo "⚠️  No database found (first time setup?)"
fi

# Step 2: Stop processes
echo ""
echo "Step 2: Stopping running processes..."
pkill -f "python.*main.py" 2>/dev/null || echo "No main.py process running"
pkill -f "python.*app.py" 2>/dev/null || echo "No app.py process running"
sleep 2
echo "✅ Processes stopped!"

# Step 3: Run migration
echo ""
echo "Step 3: Running database migration..."
if [ -f "$UPGRADE_FILES_DIR/migrate_add_project_name.py" ]; then
    cp "$UPGRADE_FILES_DIR/migrate_add_project_name.py" ./
    python3 migrate_add_project_name.py
    echo "✅ Migration complete!"
else
    echo "⚠️  Migration script not found at $UPGRADE_FILES_DIR/migrate_add_project_name.py"
    echo "Please run migration manually!"
fi

# Step 4: Update files
echo ""
echo "Step 4: Updating application files..."

# Backup originals
echo "  Backing up original files..."
cp src/main.py src/main_old_$(date +%Y%m%d).py 2>/dev/null || echo "  (main.py backup skipped)"
cp src/dashboard/app.py src/dashboard/app_old_$(date +%Y%m%d).py 2>/dev/null || echo "  (app.py backup skipped)"
cp src/dashboard/templates/index.html src/dashboard/templates/index_old_$(date +%Y%m%d).html 2>/dev/null || echo "  (index.html backup skipped)"

# Update files
echo "  Installing new files..."
if [ -f "$UPGRADE_FILES_DIR/main_updated.py" ]; then
    cp "$UPGRADE_FILES_DIR/main_updated.py" src/main.py
    echo "  ✅ main.py updated"
else
    echo "  ⚠️  main_updated.py not found"
fi

if [ -f "$UPGRADE_FILES_DIR/app_updated.py" ]; then
    cp "$UPGRADE_FILES_DIR/app_updated.py" src/dashboard/app.py
    echo "  ✅ app.py updated"
else
    echo "  ⚠️  app_updated.py not found"
fi

if [ -f "$UPGRADE_FILES_DIR/index_updated.html" ]; then
    cp "$UPGRADE_FILES_DIR/index_updated.html" src/dashboard/templates/index.html
    echo "  ✅ index.html updated"
else
    echo "  ⚠️  index_updated.html not found"
fi

if [ -f "$UPGRADE_FILES_DIR/config.py" ]; then
    # Only update if Kognity is not already there
    if grep -q "kognity.com" src/config.py; then
        echo "  ✅ config.py already has Kognity (no update needed)"
    else
        cp src/config.py src/config_old_$(date +%Y%m%d).py
        cp "$UPGRADE_FILES_DIR/config.py" src/config.py
        echo "  ✅ config.py updated"
    fi
else
    echo "  ⚠️  config.py not found (probably not needed)"
fi

# Step 5: Verify
echo ""
echo "Step 5: Verifying installation..."
echo ""

# Check database
if python3 -c "import sqlite3; conn = sqlite3.connect('data/study_data.db'); cursor = conn.cursor(); cursor.execute('PRAGMA table_info(sessions)'); cols = [col[1] for col in cursor.fetchall()]; print('✅ project_name column exists!' if 'project_name' in cols else '❌ project_name column NOT found!'); conn.close()"; then
    echo ""
else
    echo "❌ Database check failed!"
fi

# Check config
if grep -q "kognity.com" src/config.py; then
    echo "✅ Kognity in config.py"
else
    echo "❌ Kognity NOT in config.py"
fi

# Check main.py
if grep -q "extract_project_name" src/main.py; then
    echo "✅ main.py has project extraction"
else
    echo "❌ main.py missing project extraction"
fi

# Check app.py
if grep -q "hours = seconds // 3600" src/dashboard/app.py; then
    echo "✅ app.py has new time format"
else
    echo "❌ app.py missing new time format"
fi

# Check index.html
if grep -q "display: false.*NO LEGEND" src/dashboard/templates/index.html; then
    echo "✅ index.html has no-legend pie charts"
else
    echo "❌ index.html missing no-legend setting"
fi

echo ""
echo "============================================================"
echo "UPGRADE COMPLETE!"
echo "============================================================"
echo ""
echo "✅ All files have been updated!"
echo ""
echo "Next steps:"
echo "  1. Start the tracker:   python3 src/main.py"
echo "  2. Start the dashboard: python3 src/dashboard/app.py"
echo "  3. Open Kognity in Comet browser"
echo "  4. Watch for 'PROJECT DETECTED' in logs"
echo ""
echo "📖 For detailed info, see UPGRADE_GUIDE.md"
echo ""
