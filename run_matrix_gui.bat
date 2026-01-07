@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo [*] Zapret GUI - Starting...
echo.

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Install from https://python.org
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check CustomTkinter
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing CustomTkinter...
    python -m pip install --quiet customtkinter pillow psutil
    if %errorlevel% neq 0 (
        echo [ERROR] Installation failed!
        pause
        exit /b 1
    )
    echo [OK] CustomTkinter installed
)

REM Check winws.exe
if not exist "bin\winws.exe" (
    echo [ERROR] bin\winws.exe not found!
    echo Make sure all Zapret files are extracted.
    pause
    exit /b 1
)

echo [OK] All checks passed
echo.
echo [*] Starting GUI...
echo.

REM Start GUI
start "Zapret GUI" python zapret_matrix_gui.py

timeout /t 2 >nul
echo [OK] GUI launched!
echo.
echo Close this window if GUI opened successfully.
pause
