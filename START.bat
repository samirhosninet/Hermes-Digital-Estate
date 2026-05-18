@echo off
chcp 65001 >nul 2>&1
setlocal
title Hermes Digital State - Stack Installer

echo.
echo  ===================================================
echo   Hermes Digital State - Stack Installer
echo  ===================================================
echo.
echo  This starts a local Web UI that installs/checks:
echo    1. Hermes Agent
echo    2. Hermes Workspace
echo    3. Digital State profile
echo.

where powershell >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Windows PowerShell was not found.
    echo  This installer requires built-in Windows PowerShell.
    echo.
    pause
    exit /b 1
)

set "BOOTSTRAP=%~dp0scripts\bootstrap\windows_bootstrap.ps1"
if not exist "%BOOTSTRAP%" (
    echo  [ERROR] Bootstrap script not found:
    echo  %BOOTSTRAP%
    echo.
    pause
    exit /b 1
)

echo  Starting local installer UI...
echo  Keep this window open while installation is running.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%BOOTSTRAP%"
set "RESULT=%ERRORLEVEL%"

if not "%RESULT%"=="0" (
    echo.
    echo  [ERROR] Installer stopped with code %RESULT%.
    echo  Review the messages above, then run START.bat again.
    echo.
    pause
)

exit /b %RESULT%
