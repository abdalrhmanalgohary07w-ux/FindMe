@echo off
TITLE FindMe Backend Setup
setlocal

echo ====================================================
echo   FindMe Backend Setup - Automated Installer
echo ====================================================

:: 1. Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9+ and add to PATH.
    pause
    exit /b
)

:: 2. Venv
if not exist "venv" (
    echo [2/5] Creating Virtual Environment...
    python -m venv venv
) else (
    echo [2/5] venv already exists.
)

:: 3. Install Requirements
echo [3/5] Installing dependencies...
call venv\Scripts\activate.bat

:: Upgrade pip first for better wheel discovery
call python -m pip install --upgrade pip

if exist "packages" (
    echo [INFO] Offline folder 'packages' found. Installing locally...
    call pip install --no-index --find-links=./packages -r requirements.txt
) else (
    echo [INFO] No 'packages' folder found. Installing from internet...
    call pip install --default-timeout=100 --prefer-binary -r requirements.txt
)

if %errorlevel% neq 0 (
    echo.
    echo [!] ERROR: Installation failed. 
    echo [!] If you are offline, ensure the 'packages' folder is complete.
    echo.
    pause
    exit /b
)

:: 4. Migrations
echo [4/5] Setting up database...
call python manage.py makemigrations
call python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Database setup failed. Ensure you are in the correct folder.
    pause
    exit /b
)

:: 5. Run
echo [5/5] Everything is ready!
echo Visit http://127.0.0.1:8000/ to verify.
call python manage.py runserver

pause
