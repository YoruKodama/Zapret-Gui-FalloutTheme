@echo off
chcp 65001 > nul
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   Запуск Zapret GUI из исходников           ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python не найден!
        echo [*] Установите Python 3.8+ или используйте ZapretMatrixGUI.exe
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo [OK] Python найден

REM Установка зависимостей
echo.
echo [*] Проверка зависимостей...
%PYTHON_CMD% -m pip install customtkinter pillow psutil --quiet --disable-pip-version-check 2>nul
if %errorlevel% equ 0 (
    echo [OK] Зависимости установлены
) else (
    echo [!] Не удалось установить зависимости
)

echo.
echo [*] Запускаем GUI...
echo.
%PYTHON_CMD% zapret_matrix_gui.py
