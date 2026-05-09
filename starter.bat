@echo off
set VENV_PYTHON="%~dp0.venv\Scripts\python.exe"
set MAIN_SCRIPT="%~dp0main.py"

if not exist %VENV_PYTHON% (
    echo Error: .venv not found in %~dp0
    pause
    exit /b
)

%VENV_PYTHON% %MAIN_SCRIPT% %*