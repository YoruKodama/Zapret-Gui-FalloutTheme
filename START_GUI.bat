@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ═══════════════════════════════════════════════════════════
echo    Zapret Matrix GUI - Автоматический запуск
echo ═══════════════════════════════════════════════════════════
echo.

REM Проверка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден!
    echo.
    echo Установите Python с https://python.org
    echo При установке выберите "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

REM Автоматическая установка зависимостей
echo [*] Проверка зависимостей...
python -c "import customtkinter, PIL, psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Устанавливаю необходимые библиотеки...
    echo [*] Это может занять 1-2 минуты...
    echo.
    
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements_gui.txt --quiet
    
    if %errorlevel% neq 0 (
        echo [ERROR] Не удалось установить зависимости!
        echo [*] Попробуйте вручную: pip install -r requirements_gui.txt
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] Все зависимости установлены!
    echo.
) else (
    echo [OK] Все зависимости уже установлены
    echo.
)

REM Проверка файлов Zapret
if not exist "bin\winws.exe" (
    echo [WARNING] bin\winws.exe не найден!
    echo [*] Убедитесь что все файлы распакованы
    echo.
)

echo [*] Запускаю GUI...
echo.

REM Запуск GUI
start "Zapret Matrix GUI" python zapret_matrix_gui.py

timeout /t 2 >nul
echo [OK] GUI запущен!
echo.
echo Если окно GUI открылось, можете закрыть это окно.
echo.
pause
