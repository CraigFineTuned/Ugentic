@echo off

REM This script sets up and runs the Ugentic application.

REM Check if the virtual environment already exists.
IF NOT EXIST .\venv (
    echo Creating Python virtual environment...
    python -m venv .venv
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment. Make sure Python is installed and in your PATH.
        pause
        exit /b %ERRORLEVEL%
    )
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment.
echo Activating virtual environment...
call .\venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

REM Install dependencies.
echo Installing dependencies from requirements.txt...
_pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies.
    pause
    exit /b %ERRORLEVEL%
)

REM Run the application.
echo Starting the Ugentic application...
echo To stop the application, press Ctrl+C in the terminal.
python app.py

REM Deactivate the virtual environment (optional, as the script ends here).
call .\venv\Scripts\deactivate.bat

echo Application finished.
pause
