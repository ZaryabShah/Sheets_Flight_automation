@echo off
echo Running Delta Flight Automation...
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Starting automation...
python delta_flight_automation_advanced.py

if errorlevel 1 (
    echo Error: Automation failed
    pause
    exit /b 1
)

echo Automation completed!
pause
