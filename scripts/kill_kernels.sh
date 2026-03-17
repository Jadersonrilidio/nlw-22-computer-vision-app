#!/bin/bash

echo "Stopping all hanging Python kernels..."

# Kill ipykernel processes
pkill -9 -f ipykernel_launcher
pkill -9 -f jupyter

# Optional: Kill any stray python processes from .venv
pkill -9 -f ".venv/bin/python"

echo "Done! All kernels have been terminated."
echo "You can now try to open your notebook and reconnect to the .venv kernel."
