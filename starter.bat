@echo off
set VENV_DIR=%~dp0.venv
set VENV_PYTHON="%VENV_DIR%\Scripts\python.exe"
set REQS="%~dp0requirements.txt"
set MAIN_SCRIPT="%~dp0main.py"

if not exist %VENV_DIR% (
    echo .venv not found. Creating...
    python -m venv %VENV_DIR%

    if errorlevel 1 (
        echo Error while creating .venv
        pause
        exit /b
    )
    echo Installing requirements...
    if exist %REQS% (
        %VENV_PYTHON% -m pip install --upgrade pip
        %VENV_PYTHON% -m pip install -r %REQS%
    ) else (
        echo requirements.txt not found
    )
    echo .venv is ready
)

echo Running %MAIN_SCRIPT%...
%VENV_PYTHON% %MAIN_SCRIPT% %

if errorlevel 1 (
    echo error while running script
    pause
)
