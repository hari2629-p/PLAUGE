@echo off
title PLAUGE Launcher 🔴⚪
color 0c

echo.
echo ===================================================
echo      PLAUGE - Arsenal Edition 🔴⚪
echo      Unified Plagiarism ^& AI Detector
echo ===================================================
echo.

REM 1. Activate Environment
if exist ".venv\Scripts\activate.bat" (
    echo [1/3] Activating Virtual Environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: .venv not found! Using global python environment...
)

REM 1.5. Build React Frontend
if not exist "frontend1\dist\index.html" (
    echo [2/4] Building React frontend for the first time...
    cd frontend1
    call npm install
    call npm run build
    cd ..
) else (
    echo [2/4] React Frontend already built.
)

REM 2. Open Frontend
echo [3/4] Opening Frontend Interface (http://localhost:5000)...
start http://localhost:5000

REM 3. Start Backend
echo [4/4] Starting AI Backend Engine...
echo.
echo (Keep this window open while using the app)
echo.
set PYTHONIOENCODING=utf-8
python backend\api\app.py

pause
