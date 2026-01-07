@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ═══════════════════════════════════════════════════════════════
echo    Zapret Matrix GUI - Сборка исполняемого файла
echo ═══════════════════════════════════════════════════════════════
echo.

REM Проверка Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python не найден!
    echo [*] Установите Python с https://python.org
    pause
    exit /b 1
)

echo [OK] Python найден
echo.

REM Проверка зависимостей
echo [*] Проверка зависимостей...
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Устанавливаю зависимости...
    python -m pip install --quiet -r requirements_gui.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Не удалось установить зависимости!
        pause
        exit /b 1
    )
)

echo [OK] Зависимости установлены
echo.

REM Запуск скрипта сборки
echo [*] Запускаю сборку...
echo.
python build_exe.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Сборка завершилась с ошибкой!
    pause
    exit /b 1
)

echo.
echo [OK] Сборка завершена успешно!
echo [*] Исполняемый файл: dist\ZapretMatrixGUI.exe
echo.

pause
