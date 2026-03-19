#!/bin/bash

# --- Vision Gesture Pro: Port Liberator Script ---
# This script finds and stops any process running on port 5001.
# This prevents the "Address already in use" error when restarting the app.

# 1. Define the port we want to clear
PORT=5001

# 2. Find the Process ID (PID) currently using that port.
# 'lsof' (List Open Files) with '-t' gives us just the ID number.
# '-i :5001' filters for the specific port.
PID=$(lsof -t -i:$PORT)

# 3. Check if we actually found a process
if [ -z "$PID" ]; then
    echo "✅ No process found on port $PORT. Everything is clear!"
else
    # 4. If a process exists, tell the user and terminate it
    echo "⚠️ Found process $PID running on port $PORT. Safely closing it..."
    
    # 'kill -9' forcefully stops the process by its ID
    kill -9 $PID
    
    # 5. Confirm completion
    if [ $? -eq 0 ]; then
        echo "🚀 Port $PORT has been successfully liberated! You can now run 'uv run python app.py'."
    else
        echo "❌ Something went wrong. You might need to run this script with 'sudo'."
    fi
fi
