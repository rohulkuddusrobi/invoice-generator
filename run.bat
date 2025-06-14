@echo off
echo 🚀 Starting Professional Invoice Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import fpdf" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installing required dependencies...
    pip install fpdf2 pillow
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        echo Please run install.bat first
        pause
        exit /b 1
    )
)

echo ✅ Starting application...
echo.
python main.py

pause
