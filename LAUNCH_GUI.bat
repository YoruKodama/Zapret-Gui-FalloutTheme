@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║            ZAPRET MATRIX GUI - ЗАПУСК                    ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [✗] Python не найден!
    echo.
    echo Установите Python с https://python.org
    echo При установке выберите "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [✓] Python найден
echo.

REM Автоматическая установка зависимостей
echo [*] Проверка зависимостей...
python -c "import customtkinter, PIL, psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Устанавливаю необходимые библиотеки...
    echo [*] Подождите 1-2 минуты...
    echo.
    
    python -m pip install --upgrade pip --quiet 2>nul
    python -m pip install customtkinter pillow psutil --quiet
    
    if %errorlevel% neq 0 (
        echo [✗] Автоматическая установка не удалась
        echo.
        echo Попробуйте вручную:
        echo     pip install customtkinter pillow psutil
        echo.
        pause
        exit /b 1
    )
    
    echo [✓] Все библиотеки установлены!
    echo.
) else (
    echo [✓] Все зависимости на месте
    echo.
)

echo [*] Запускаю GUI...
echo.

REM Запуск GUI
start "Zapret Matrix GUI" python zapret_matrix_gui.py

timeout /t 2 >nul
echo [✓] GUI запущен!
echo.
echo ════════════════════════════════════════════════════════════
echo  Если окно открылось, можете закрыть эту консоль
echo ════════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul
exit /b 0
