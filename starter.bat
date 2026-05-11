@echo off
set VENV_DIR=%~dp0.venv
set VENV_PYTHON="%VENV_DIR%\Scripts\python.exe"
set REQS="%~dp0requirements.txt"
set MAIN_SCRIPT="%~dp0main.py"
set LOGS="%~dp0bat_logs.log"

if not exist %LOGS% (
    type nul > %LOGS%
)

if not exist %VENV_DIR% (
    echo [starter.bat] .venv not found. Creating... >> %LOGS%
    python -m venv %VENV_DIR%

    if errorlevel 1 (
        echo [starter.bat] Error while creating .venv >> %LOGS%
        exit /b
    )
    echo [starter.bat] Installing requirements... >> %LOGS%
    if exist %REQS% (
        %VENV_PYTHON% -m pip install --upgrade pip >> %LOGS% 2>&1
        %VENV_PYTHON% -m pip install -r %REQS% >> %LOGS% 2>&1
    ) else (
        echo [starter.bat] requirements.txt not found >> %LOGS%
    )
    echo [starter.bat] requirements.txt not found >> %LOGS%
)

echo [starter.bat] Running %MAIN_SCRIPT%... >> %LOGS%
%VENV_PYTHON% %MAIN_SCRIPT% %* >> %LOGS% 2>&1

if errorlevel 1 (
    echo [starter.bat] Error while running script >> %LOGS%
)