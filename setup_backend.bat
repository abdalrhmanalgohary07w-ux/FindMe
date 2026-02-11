@echo off
echo ==========================================
echo    FindMe Backend Auto-Setup Tool
echo ==========================================
echo.

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed! 
    echo Please install Python 3.10 from https://www.python.org/downloads/
    pause
    exit /b
)

:: 2. Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [1/4] Creating Virtual Environment...
    python -m venv venv
) else (
    echo [SKIP] Virtual Environment already exists.
)

:: 3. Install Requirements using venv's python
echo [2/4] Installing Required Libraries (This may take a few minutes)...
:: Clean up old conflicting versions
venv\Scripts\python.exe -m pip uninstall -y tensorflow keras tf-keras mtcnn
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

:: 4. Setup Database & Migrations
echo [3/4] Preparing Database...
venv\Scripts\python.exe manage.py makemigrations api
venv\Scripts\python.exe manage.py migrate

:: 5. Run Server
echo [4/4] Starting FindMe Server...
echo.
echo ==========================================
echo    SERVER IS STARTING AT http://127.0.0.1:8000
echo ==========================================
venv\Scripts\python.exe manage.py runserver
pause
