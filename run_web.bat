@echo off
echo 🌐 Starting Invoice Generator Web Interface...
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
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        echo Please run install.bat first
        pause
        exit /b 1
    )
)

echo ✅ Starting web server...
echo.
echo 📱 The application will open at: http://localhost:5000
echo 🔄 Press Ctrl+C to stop the server
echo.
python web_app.py

pause
