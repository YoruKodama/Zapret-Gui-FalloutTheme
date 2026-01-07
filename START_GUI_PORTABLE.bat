@echo off
chcp 65001 > nul
cd /d "%~dp0"

REM ═══════════════════════════════════════════════════════════════
REM    Zapret Matrix GUI - Portable версия (без Python)
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo    Zapret Matrix GUI - Запуск
echo ═══════════════════════════════════════════════════════════════
echo.

REM Проверка наличия .exe файла
if exist "dist\ZapretMatrixGUI.exe" (
    echo [*] Запускаю portable версию...
    echo [OK] Python НЕ требуется!
    echo.
    start "" "dist\ZapretMatrixGUI.exe"
    timeout /t 2 >nul
    echo [OK] GUI запущен!
    exit /b 0
)

if exist "ZapretMatrixGUI.exe" (
    echo [*] Запускаю portable версию...
    echo [OK] Python НЕ требуется!
    echo.
    start "" "ZapretMatrixGUI.exe"
    timeout /t 2 >nul
    echo [OK] GUI запущен!
    exit /b 0
)

REM Если .exe не найден, пробуем обычный запуск
echo [!] Portable версия не найдена
echo [*] Ищу Python версию...
echo.

if not exist "zapret_matrix_gui.py" (
    echo [ERROR] GUI файлы не найдены!
    echo.
    echo [*] Для создания portable версии запустите:
    echo     build_exe.bat
    echo.
    pause
    exit /b 1
)

REM Проверка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден!
    echo.
    echo [*] Варианты решения:
    echo     1. Установите Python с https://python.org
    echo     2. Используйте portable версию (ZapretMatrixGUI.exe)
    echo.
    echo [*] Для создания portable версии запустите:
    echo     build_exe.bat
    echo.
    pause
    exit /b 1
)

echo [OK] Python найден
echo [*] Проверяю зависимости...
echo.

REM Автоматическая установка зависимостей
python -c "import customtkinter, PIL, psutil" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Устанавливаю необходимые библиотеки...
    echo [*] Это займет 1-2 минуты...
    echo.
    
    python -m pip install --upgrade pip --quiet
    python -m pip install -r requirements_gui.txt --quiet
    
    if %errorlevel% neq 0 (
        echo [ERROR] Не удалось установить зависимости!
        echo.
        pause
        exit /b 1
    )
    
    echo [OK] Зависимости установлены!
    echo.
)

echo [*] Запускаю Python версию...
echo.

start "Zapret Matrix GUI" python zapret_matrix_gui.py

timeout /t 2 >nul

echo [OK] GUI запущен!
echo.
echo [TIP] Для создания версии без Python запустите: build_exe.bat
echo.
pause
