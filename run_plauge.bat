@echo off
title PLAUGE Launcher 🔴⚪
color 0c

echo.
echo ===================================================
echo      PLAUGE - Arsenal Edition 🔴⚪
echo      Unified Plagiarism & AI Detector
echo ===================================================
echo.

REM 1. Activate Environment
if exist ".venv\Scripts\activate.bat" (
    echo [1/3] Activating Virtual Environment...
    call .venv\Scripts\activate.bat
) else (
    echo Error: .venv not found! Please install requirements.
    pause
    exit /b
)

REM 2. Open Frontend
echo [2/3] Opening Frontend Interface (http://localhost:5000)...
start http://localhost:5000

REM 3. Start Backend
echo [3/3] Starting AI Backend Engine...
echo.
echo (Keep this window open while using the app)
echo.
python backend\api\app.py

pause
