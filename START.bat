@echo off
chcp 65001 >nul 2>&1
setlocal
title Hermes Digital State - Setup Wizard

echo.
echo  ===================================================
echo   Hermes Digital State - Setup Wizard
echo  ===================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found!
    echo.
    echo  Please install Python 3.10+ from:
    echo  https://www.python.org/downloads/
    echo.
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set pyver=%%v
echo  Python found: %pyver%

set "WIZARD_DIR=%~dp0"
set "HERMES_WIZARD_LOG=%TEMP%\hermes-digital-state-wizard.log"
if exist "%HERMES_WIZARD_LOG%" del "%HERMES_WIZARD_LOG%" >nul 2>&1

echo  Starting wizard in the background...
echo  Log: %HERMES_WIZARD_LOG%
start "" /b python "%WIZARD_DIR%wizard.py" --no-browser > "%HERMES_WIZARD_LOG%" 2>&1

for /f "usebackq delims=" %%u in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$log=$env:HERMES_WIZARD_LOG; $deadline=(Get-Date).AddSeconds(20); do { Start-Sleep -Milliseconds 500; if (Test-Path -LiteralPath $log) { $text=Get-Content -LiteralPath $log -Raw; $m=[regex]::Match($text, 'http://127\.0\.0\.1:\d+'); if ($m.Success) { try { Invoke-WebRequest -UseBasicParsing -Uri ($m.Value + '/api/info') -TimeoutSec 2 | Out-Null; Write-Output $m.Value; exit 0 } catch {} }; if ($text -match 'Traceback|RuntimeError|ValueError|Error:') { exit 2 } } } while ((Get-Date) -lt $deadline); exit 1"`) do set "WIZARD_URL=%%u"

if not defined WIZARD_URL (
    echo.
    echo  [ERROR] Wizard did not become ready.
    echo  Review the log:
    echo  %HERMES_WIZARD_LOG%
    echo.
    if exist "%HERMES_WIZARD_LOG%" type "%HERMES_WIZARD_LOG%"
    echo.
    pause
    exit /b 1
)

echo  Wizard ready: %WIZARD_URL%
start "" "%WIZARD_URL%"
exit /b 0
