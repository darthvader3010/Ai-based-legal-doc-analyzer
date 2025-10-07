@echo off
REM Setup script for AI-Based Legal Document Analyzer (Windows)
REM This script will set up the environment and install dependencies

echo ==========================================
echo AI-Based Legal Document Analyzer
echo Setup Script (Windows)
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

python --version
echo.

REM Check pip
echo Checking for pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not installed.
    echo Please install pip or reinstall Python with pip included.
    pause
    exit /b 1
)

echo [OK] pip is installed
echo.

REM Ask about virtual environment
set /p CREATE_VENV="Do you want to create a virtual environment? (recommended) [Y/n]: "
if /i "%CREATE_VENV%"=="n" goto :install_deps

echo Creating virtual environment...
python -m venv venv

echo [OK] Virtual environment created
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo [OK] Virtual environment activated
echo.

:install_deps
REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
echo.

python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo [OK] Dependencies installed
echo.

REM Create uploads directory
echo Creating uploads directory...
if not exist "uploads" mkdir uploads
echo [OK] Uploads directory created
echo.

REM Run tests
echo Running tests to verify installation...
python -m pytest test_analyzer.py -v --tb=short

if errorlevel 1 (
    echo.
    echo ==========================================
    echo [ERROR] Setup failed - tests did not pass
    echo ==========================================
    echo.
    echo Please check the error messages above and try again.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [OK] Setup completed successfully!
echo ==========================================
echo.
echo You can now use the analyzer in three ways:
echo.
echo 1. Web Application:
echo    python app.py
echo    Then visit: http://localhost:5000
echo.
echo 2. Command Line:
echo    python cli.py analyze document.pdf
echo    python cli.py search document.pdf --keywords "liability,warranty"
echo.
echo 3. Python API:
echo    See example_usage.py for code examples
echo.
echo For more information, see README.md
echo.

if /i not "%CREATE_VENV%"=="n" (
    echo Note: To activate the virtual environment in future sessions, run:
    echo    venv\Scripts\activate.bat
    echo.
)

pause
