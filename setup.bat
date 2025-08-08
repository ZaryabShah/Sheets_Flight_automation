@echo off
echo Installing Delta Flight Automation Requirements...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed ✓

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

echo ================================================
echo Setup completed successfully! ✓
echo ================================================
echo.
echo To run the automation:
echo   python delta_flight_automation_advanced.py
echo.
echo For basic version:
echo   python delta_flight_automation.py
echo.
pause
