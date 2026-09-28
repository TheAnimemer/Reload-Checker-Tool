@echo off
title Pokemon Team Finder
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 main.py
    goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python main.py
    goto done
)

echo.
echo Python is not installed.
echo Install it from https://www.python.org/downloads/
echo IMPORTANT: tick "Add python.exe to PATH" on the first installer screen.
echo Then double-click run.bat again.

:done
echo.
pause
