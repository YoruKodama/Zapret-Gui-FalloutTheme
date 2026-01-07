@REM Запуск Matrix GUI
@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

cd /d "%~dp0"

:menu
cls
color 0A
echo.
echo ╔════════════════════════════════════════════╗
echo ║       ⚡ ZAPRET MATRIX GUI ⚡               ║
echo ╚════════════════════════════════════════════╝
echo.
echo 1. ⚡ Запустить Matrix GUI
echo 2. 📦 Установить зависимости
echo 3. 📖 Открыть документацию
echo 4. 📁 Открыть папку проекта
echo 5. ❌ Выход
echo.
set /p choice="Выберите опцию (1-5): "

if "%choice%"=="1" goto run_matrix_gui
if "%choice%"=="2" goto install_deps
if "%choice%"=="3" goto open_docs
if "%choice%"=="4" goto open_folder
if "%choice%"=="5" goto exit
goto invalid_choice

:run_matrix_gui
echo.
echo ⚡ Запуск Matrix GUI...
call run_matrix_gui.bat
goto menu

:install_deps
echo.
echo 📦 Установка зависимостей...
call install_dependencies.bat
pause
goto menu

:open_docs
echo.
echo 📖 Открытие документации...
if exist MATRIX_GUI_README.md (
    start notepad MATRIX_GUI_README.md
) else if exist MATRIX_GUI_START.txt (
    start notepad MATRIX_GUI_START.txt
) else (
    echo ❌ Файл документации не найден
)
pause
goto menu

:open_folder
echo.
echo 📁 Открытие папки проекта...
start .
pause
goto menu

:invalid_choice
echo.
echo ❌ Неверный выбор, пожалуйста попробуйте снова
pause
goto menu

:exit
color
exit /b 0
