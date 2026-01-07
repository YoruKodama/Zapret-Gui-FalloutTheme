@echo off
cd /d "%~dp0"
echo Starting Zapret GUI...
python zapret_matrix_gui.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start GUI
    echo.
    echo Check:
    echo 1. Python is installed
    echo 2. Run: python -m pip install customtkinter pillow psutil
    echo 3. Run as Administrator
    echo.
    pause
)
