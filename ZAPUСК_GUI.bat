@echo off
chcp 65001 > nul
cd /d "%~dp0"

REM ═══════════════════════════════════════════════════════════════
REM    Zapret Matrix GUI - Универсальный запуск
REM    Все устанавливается автоматически!
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                                                           ║
echo ║            ZAPRET MATRIX GUI - ЗАПУСК                    ║
echo ║                                                           ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Шаг 1: Проверка Portable версии
if exist "ZapretMatrixGUI.exe" (
    echo [✓] Найдена Portable версия (.exe)
    echo [*] Python НЕ требуется!
    echo [*] Запускаю...
    echo.
    start "" "ZapretMatrixGUI.exe"
    timeout /t 2 >nul
    echo [OK] GUI запущен!
    goto :end
)

if exist "dist\ZapretMatrixGUI.exe" (
    echo [✓] Найдена Portable версия (dist/.exe)
    echo [*] Python НЕ требуется!
    echo [*] Запускаю...
    echo.
    start "" "dist\ZapretMatrixGUI.exe"
    timeout /t 2 >nul
    echo [OK] GUI запущен!
    goto :end
)

REM Шаг 2: Запуск Python версии с автоустановкой
echo [!] Portable версия не найдена
echo [*] Использую Python версию...
echo.

REM Проверка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [✗] Python не найден!
    echo.
    echo ╔═══════════════════════════════════════════════════════════╗
    echo ║  ЧТО ДЕЛАТЬ?                                              ║
    echo ╠═══════════════════════════════════════════════════════════╣
    echo ║                                                           ║
    echo ║  ВАРИАНТ 1 (Рекомендуется):                              ║
    echo ║  - Скачайте готовый ZapretMatrixGUI.exe                  ║
    echo ║  - Не требует установки Python                           ║
    echo ║                                                           ║
    echo ║  ВАРИАНТ 2:                                               ║
    echo ║  - Установите Python: https://python.org                 ║
    echo ║  - При установке выберите "Add Python to PATH"           ║
    echo ║  - Перезапустите этот файл                               ║
    echo ║                                                           ║
    echo ╚═══════════════════════════════════════════════════════════╝
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
    echo [!] Необходимо установить библиотеки
    echo [*] Устанавливаю автоматически...
    echo [*] Подождите 1-2 минуты...
    echo.
    
    python -m pip install --upgrade pip --quiet 2>nul
    python -m pip install customtkinter pillow psutil --quiet
    
    if %errorlevel% neq 0 (
        echo [✗] Автоматическая установка не удалась
        echo.
        echo [*] Попробуйте вручную:
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

REM Проверка файлов Zapret
if not exist "bin\winws.exe" (
    echo [!] ВНИМАНИЕ: bin\winws.exe не найден
    echo [*] GUI запустится, но обход может не работать
    echo.
)

echo [*] Запускаю GUI...
echo.

REM Запуск GUI
start "Zapret Matrix GUI" python zapret_matrix_gui.py

timeout /t 2 >nul
echo [✓] GUI запущен!

:end
echo.
echo ════════════════════════════════════════════════════════════
echo  Если окно открылось, можете закрыть эту консоль
echo ════════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul
exit /b 0
