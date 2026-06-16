@echo off
REM Startup script for Text Classification Project (Windows)
REM Usage: start.bat [flask|streamlit|both|docker]

setlocal enabledelayedexpansion

REM Colors using cls and title (limited on Windows CMD)
REM We'll use simple text output with symbols

cd /d "%~dp0"

echo.
echo ============================================================================
echo      Text Classification with TensorFlow - Startup Script (Windows)
echo ============================================================================
echo.

REM Check command line argument
if "%1"=="" (
    call :show_help
    exit /b 0
)

if /i "%1"=="flask" (
    call :start_flask
    exit /b !errorlevel!
) else if /i "%1"=="streamlit" (
    call :start_streamlit
    exit /b !errorlevel!
) else if /i "%1"=="both" (
    call :start_both
    exit /b !errorlevel!
) else if /i "%1"=="docker" (
    call :start_docker
    exit /b !errorlevel!
) else if /i "%1"=="help" (
    call :show_help
    exit /b 0
) else (
    echo ERROR: Unknown option: %1
    call :show_help
    exit /b 1
)

REM ============================================================================
REM Function to check model files
REM ============================================================================
:check_model_files
if not exist "saved_models\text_classification_model.h5" (
    echo ERROR: Model file not found: saved_models\text_classification_model.h5
    echo Please run the Jupyter notebook first to train and save the model.
    exit /b 1
)
if not exist "saved_models\tokenizer.pickle" (
    echo ERROR: Tokenizer file not found: saved_models\tokenizer.pickle
    exit /b 1
)
if not exist "saved_models\config.pickle" (
    echo ERROR: Config file not found: saved_models\config.pickle
    exit /b 1
)
exit /b 0

REM ============================================================================
REM Function to check dependencies
REM ============================================================================
:check_dependencies
echo Checking dependencies...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
echo OK: %PYTHON_VER%

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    exit /b 1
)
echo OK: pip is installed

REM Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo OK: Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo OK: Virtual environment activated

REM Check TensorFlow
python -c "import tensorflow" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements_deployment.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        exit /b 1
    )
    echo OK: Dependencies installed
) else (
    echo OK: All required packages are installed
)

exit /b 0

REM ============================================================================
REM Function to start Flask API
REM ============================================================================
:start_flask
echo Starting Flask API...
echo.

call :check_model_files
if errorlevel 1 exit /b 1

call :check_dependencies
if errorlevel 1 exit /b 1

echo OK: Starting Flask API on http://localhost:5000
echo.
python flask_app.py
exit /b !errorlevel!

REM ============================================================================
REM Function to start Streamlit app
REM ============================================================================
:start_streamlit
echo Starting Streamlit app...
echo.

call :check_model_files
if errorlevel 1 exit /b 1

call :check_dependencies
if errorlevel 1 exit /b 1

echo OK: Starting Streamlit app on http://localhost:8501
echo.
streamlit run streamlit_app.py
exit /b !errorlevel!

REM ============================================================================
REM Function to start both
REM ============================================================================
:start_both
echo Starting both Flask and Streamlit...
echo.

call :check_dependencies
if errorlevel 1 exit /b 1

echo OK: Starting Flask API in background...
start "Flask API" python flask_app.py

timeout /t 2 /nobreak

echo OK: Starting Streamlit app...
streamlit run streamlit_app.py
exit /b !errorlevel!

REM ============================================================================
REM Function to start Docker
REM ============================================================================
:start_docker
echo Starting with Docker...
echo.

where docker >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker from https://www.docker.com
    exit /b 1
)

where docker-compose >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed
    exit /b 1
)

echo OK: Docker found
echo.

echo Building Docker image...
docker-compose build
if errorlevel 1 (
    echo ERROR: Failed to build Docker image
    exit /b 1
)

echo.
echo Starting containers...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start containers
    exit /b 1
)

echo.
echo OK: Containers started successfully!
echo.
echo Services available at:
echo   API:      http://localhost:5000
echo   Streamlit: http://localhost:8501
echo.
echo View logs:
echo   Flask:     docker-compose logs -f flask-api
echo   Streamlit: docker-compose logs -f streamlit-app
echo.
echo Stop containers:
echo   docker-compose down
echo.
exit /b 0

REM ============================================================================
REM Function to show help
REM ============================================================================
:show_help
echo.
echo Text Classification Project - Startup Script
echo.
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   flask       Start Flask REST API only
echo   streamlit   Start Streamlit web app only
echo   both        Start both Flask and Streamlit locally
echo   docker      Start both using Docker Compose
echo   help        Show this help message
echo.
echo Examples:
echo   %0 flask            # Start Flask API
echo   %0 streamlit       # Start Streamlit web app
echo   %0 docker          # Start with Docker
echo.
echo Default (no arguments): Show this help message
echo.
exit /b 0
