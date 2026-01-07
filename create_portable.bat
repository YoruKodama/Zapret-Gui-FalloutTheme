@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ═══════════════════════════════════════════════════════════════
echo    Zapret Matrix GUI - Создание Portable пакета
echo ═══════════════════════════════════════════════════════════════
echo.

REM Проверка что .exe существует
if not exist "dist\ZapretMatrixGUI.exe" (
    echo [ERROR] Файл dist\ZapretMatrixGUI.exe не найден!
    echo [*] Сначала запустите build_exe.bat
    pause
    exit /b 1
)

REM Создание папки для дистрибутива
set "PACKAGE_NAME=ZapretMatrixGUI_Portable"
set "TIMESTAMP=%date:~-4%-%date:~3,2%-%date:~0,2%_%time:~0,2%-%time:~3,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"
set "PACKAGE_DIR=%PACKAGE_NAME%_%TIMESTAMP%"

echo [*] Создание папки: %PACKAGE_DIR%
if exist "%PACKAGE_DIR%" rd /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

echo [*] Копирование файлов...

REM Копируем .exe
echo [*] Копирую ZapretMatrixGUI.exe...
copy "dist\ZapretMatrixGUI.exe" "%PACKAGE_DIR%\" > nul

REM Копируем все .bat файлы
echo [*] Копирую .bat файлы...
copy "service.bat" "%PACKAGE_DIR%\" > nul
copy "general*.bat" "%PACKAGE_DIR%\" > nul

REM Копируем папки
echo [*] Копирую bin/...
xcopy "bin" "%PACKAGE_DIR%\bin\" /E /I /Q > nul

echo [*] Копирую lists/...
xcopy "lists" "%PACKAGE_DIR%\lists\" /E /I /Q > nul

REM Копируем конфиг
echo [*] Копирую конфигурацию...
copy "zapret_matrix_config.json" "%PACKAGE_DIR%\" > nul

REM Копируем документацию
echo [*] Копирую документацию...
copy "QUICKSTART.md" "%PACKAGE_DIR%\" > nul
copy "USER_GUIDE_RU.txt" "%PACKAGE_DIR%\" > nul
copy "LICENSE.txt" "%PACKAGE_DIR%\" > nul

REM Создаем README для portable версии
echo [*] Создаю README...
(
echo # Zapret Matrix GUI - Portable версия
echo.
echo ## Быстрый старт
echo.
echo 1. Запустите **ZapretMatrixGUI.exe**
echo 2. Выберите стратегию ^(например, general.bat^)
echo 3. Нажмите "Запустить Zapret"
echo 4. Готово! ✨
echo.
echo ## Требования
echo.
echo - Windows 10/11
echo - Права администратора ^(для запуска сервиса^)
echo - **Python НЕ нужен!**
echo.
echo ## Содержимое
echo.
echo - `ZapretMatrixGUI.exe` - основная программа
echo - `service.bat` - сервис запрета
echo - `general*.bat` - стратегии обхода
echo - `bin/` - системные файлы WinDivert
echo - `lists/` - списки доменов и IP
echo.
echo ## Документация
echo.
echo - **QUICKSTART.md** - быстрый старт
echo - **USER_GUIDE_RU.txt** - полное руководство на русском
echo.
echo ## Проблемы?
echo.
echo Смотрите QUICKSTART.md или USER_GUIDE_RU.txt
echo.
) > "%PACKAGE_DIR%\README.txt"

REM Создаем .zip архив если есть PowerShell
echo [*] Создание .zip архива...
powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%' -DestinationPath '%PACKAGE_DIR%.zip' -Force" 2>nul
if !errorlevel! equ 0 (
    echo [OK] Архив создан: %PACKAGE_DIR%.zip
) else (
    echo [!] PowerShell не найден, архив не создан
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo [OK] Portable пакет создан успешно!
echo ═══════════════════════════════════════════════════════════════
echo.
echo [*] Папка: %PACKAGE_DIR%\
echo [*] Архив: %PACKAGE_DIR%.zip
echo.
echo [*] Содержимое готово для распространения!
echo [*] Пользователям нужен только .exe файл и структура папок.
echo.
pause
