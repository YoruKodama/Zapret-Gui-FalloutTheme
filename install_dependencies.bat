@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo ============================================
echo   УСТАНОВКА ЗАВИСИМОСТЕЙ ДЛЯ ZAPRET GUI
echo ============================================
echo.

REM Проверка Python
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ ОШИБКА: Python не найден!
    echo.
    echo Пожалуйста установите Python 3.8+
    echo https://www.python.org/downloads/
    echo.
    echo Не забудьте отметить "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✓ Python найден
python --version
echo.

echo ⏳ Обновление pip...
python -m pip install --upgrade pip -q
echo ✓ pip обновлён
echo.

echo ⏳ Установка CustomTkinter...
python -m pip install customtkinter>=5.2.0 -q
echo ✓ CustomTkinter установлен
echo.

echo ⏳ Установка Pillow...
python -m pip install pillow>=10.0.0 -q
echo ✓ Pillow установлен
echo.

echo ⏳ Установка psutil...
python -m pip install psutil>=5.9.0 -q
echo ✓ psutil установлен
echo.

echo ⏳ Установка psutil...
python -m pip install psutil>=5.9.0 -q
echo ✓ psutil установлен
echo.

echo ============================================
echo ✓ ВСЕ ЗАВИСИМОСТИ УСПЕШНО УСТАНОВЛЕНЫ!
echo ============================================
echo.
echo 🚀 Для запуска GUI используйте:
echo.
echo    run_matrix_gui.bat
echo.
echo    или
echo.
echo    GUI_MENU.bat
echo.
pause
exit /b 0
