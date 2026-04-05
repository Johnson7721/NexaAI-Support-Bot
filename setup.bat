@echo off
echo ============================================
echo   RAG Chatbot - Setup Script for Windows
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [4/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ==========================================
    echo   IMPORTANT: Open .env file and add your
    echo   Google Gemini API key!
    echo ==========================================
)

echo.
echo ============================================
echo   Setup complete!
echo.
echo   Next steps:
echo   1. Open .env and add your Gemini API key
echo   2. Run: venv\Scripts\activate
echo   3. Run: streamlit run src/app.py
echo ============================================
pause
