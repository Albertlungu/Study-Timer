#!/bin/bash

echo "🔍 Checking Accessibility Permissions..."
echo ""

# Check if Comet has accessibility permissions
echo "Checking if Comet has Accessibility permissions..."
if /usr/bin/sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "SELECT client FROM access WHERE service='kTCCServiceAccessibility' AND client LIKE '%Comet%';" 2>/dev/null | grep -q Comet; then
    echo "Comet has Accessibility permissions"
else
    echo "❌ Comet does NOT have Accessibility permissions"
    echo ""
    echo "🔧 TO FIX: Go to System Preferences → Security & Privacy → Privacy → Accessibility"
    echo "   Add Comet to the list of allowed apps"
    echo ""
fi

# Check if the Study Timer script has permissions
SCRIPT_NAME=$(basename "$0" .sh)
if /usr/bin/sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" "SELECT client FROM access WHERE service='kTCCServiceAccessibility' AND client LIKE '%python%' OR client LIKE '%Study%';" 2>/dev/null | grep -q -E "(python|Study)"; then
    echo "Study Timer appears to have Accessibility permissions"
else
    echo "❌ Study Timer does NOT have Accessibility permissions"
    echo ""
    echo "🔧 TO FIX: Go to System Preferences → Security & Privacy → Privacy → Accessibility"
    echo "   Add your Python interpreter/Terminal app to the list"
    echo ""
fi

echo "🎯 Make sure both Comet AND the terminal running the script have permissions!"
echo ""
echo "📝 After granting permissions, restart the Study Timer."
