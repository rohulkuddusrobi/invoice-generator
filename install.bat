@echo off
echo Installing Professional Invoice Generator...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Install required packages
pip install fpdf2 pillow

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed successfully!
echo.
echo You can now run the application with:
echo   python main.py
echo.
echo Or run the GUI directly with:
echo   python invoice_gui.py
echo.
pause
