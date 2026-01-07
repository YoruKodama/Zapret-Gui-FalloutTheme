@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo.
echo ═══════════════════════════════════════════════════════════════
echo    Создание дистрибутивного пакета Zapret Matrix GUI
echo ═══════════════════════════════════════════════════════════════
echo.

REM Проверка наличия .exe файла
if not exist "dist\ZapretMatrixGUI.exe" (
    echo [ERROR] ZapretMatrixGUI.exe не найден!
    echo [*] Сначала выполните сборку: build_exe.bat
    pause
    exit /b 1
)

echo [OK] Исполняемый файл найден
echo.

REM Создание папки для дистрибутива
set "DIST_DIR=ZapretMatrixGUI_Portable"
set "TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%"

if exist "%DIST_DIR%" (
    echo [*] Удаляю старую папку дистрибутива...
    rmdir /s /q "%DIST_DIR%"
)

echo [*] Создаю структуру дистрибутива...
mkdir "%DIST_DIR%" 2>nul
mkdir "%DIST_DIR%\bin" 2>nul
mkdir "%DIST_DIR%\lists" 2>nul

REM Копирование файлов
echo [*] Копирую файлы...

REM Главный .exe
copy "dist\ZapretMatrixGUI.exe" "%DIST_DIR%\" >nul
echo [OK] ZapretMatrixGUI.exe

REM Конфигурация
if exist "zapret_matrix_config.json" (
    copy "zapret_matrix_config.json" "%DIST_DIR%\" >nul
    echo [OK] zapret_matrix_config.json
)

REM Binaries
if exist "bin\winws.exe" copy "bin\winws.exe" "%DIST_DIR%\bin\" >nul
if exist "bin\WinDivert64.sys" copy "bin\WinDivert64.sys" "%DIST_DIR%\bin\" >nul
if exist "bin\WinDivert.dll" copy "bin\WinDivert.dll" "%DIST_DIR%\bin\" >nul
echo [OK] Binaries (bin/)

REM Списки доменов
xcopy "lists\*" "%DIST_DIR%\lists\" /Y /Q >nul 2>&1
echo [OK] Списки доменов (lists/)

REM Создание README для пользователей
echo [*] Создаю README...
(
echo # 🎮 Zapret Matrix GUI - Portable версия
echo.
echo ## 🚀 Быстрый старт
echo.
echo 1. **Запустите** `ZapretMatrixGUI.exe`
echo 2. **Выберите** стратегию обхода в интерфейсе
echo 3. **Нажмите** "АКТИВИРОВАТЬ"
echo 4. **Готово!** ✨
echo.
echo ## ✨ Особенности
echo.
echo - ✅ **Не требует Python** - все включено
echo - ✅ **Portable** - можно запускать с флешки
echo - ✅ **Простой интерфейс** в стиле терминала
echo - ✅ **Автоматическое управление** сервисом Zapret
echo.
echo ## ⚙️ Конфигурация
echo.
echo ### Стратегии обхода
echo.
echo Доступны через выпадающий список в GUI:
echo - **general.bat** - основная стратегия (рекомендуется)
echo - **general (ALT).bat** - альтернативная стратегия
echo - **general (ALT2-11).bat** - дополнительные варианты
echo - **general (FAKE TLS).bat** - Fake TLS методы
echo.
echo ### Параметры
echo.
echo - **IP фильтрация**: loaded (рекомендуется), none, any
echo - **Фильтр для игр**: включает UDP/TCP фильтрацию
echo - **Автозапуск**: запуск при старте системы
echo.
echo ## 📁 Структура папки
echo.
echo ```
echo ZapretMatrixGUI_Portable/
echo   ├── ZapretMatrixGUI.exe         ← Запускайте этот файл
echo   ├── zapret_matrix_config.json   ← Настройки
echo   ├── bin/                         ← Исполняемые файлы zapret
echo   │   ├── winws.exe
echo   │   └── WinDivert64.sys
echo   └── lists/                       ← Списки доменов для обхода
echo       ├── list-general.txt
echo       └── ...
echo ```
echo.
echo ## ⚠️ Требования
echo.
echo - **Windows 10/11** (64-bit)
echo - **Права администратора** (для установки сервиса)
echo - **WinDivert драйвер** (устанавливается автоматически)
echo.
echo ## 🔧 Устранение проблем
echo.
echo ### Не запускается / Ошибка при активации
echo.
echo 1. **Запускайте от имени администратора**
echo    - ПКМ на ZapretMatrixGUI.exe → "Запуск от имени администратора"
echo.
echo 2. **Проверьте антивирус**
echo    - Добавьте папку в исключения
echo    - WinDivert драйвер может блокироваться
echo.
echo 3. **Проверьте файлы**
echo    - bin/winws.exe должен существовать
echo    - bin/WinDivert64.sys должен существовать
echo.
echo ### Не работает обход
echo.
echo 1. **Попробуйте другую стратегию**
echo    - Выберите другой .bat файл из списка
echo.
echo 2. **Проверьте списки**
echo    - lists/list-general.txt должен содержать нужные домены
echo.
echo 3. **Перезапустите**
echo    - Нажмите "ДЕАКТИВАЦИЯ", затем снова "АКТИВИРОВАТЬ"
echo.
echo ## 📞 Поддержка
echo.
echo - **GitHub**: [Ссылка на репозиторий]
echo - **Оригинальный Zapret**: https://github.com/Flowseal/zapret-discord-youtube
echo.
echo ## 📜 Лицензия
echo.
echo См. LICENSE.txt
echo.
echo ---
echo.
echo **Готово!** 🎉 Запустите ZapretMatrixGUI.exe и наслаждайтесь свободным интернетом!
) > "%DIST_DIR%\README.md"
echo [OK] README.md

REM Копирование лицензии
if exist "LICENSE.txt" (
    copy "LICENSE.txt" "%DIST_DIR%\" >nul
    echo [OK] LICENSE.txt
)

REM Создание bat файла для запуска
(
echo @echo off
echo cd /d "%%~dp0"
echo start "" "ZapretMatrixGUI.exe"
) > "%DIST_DIR%\Запустить GUI.bat"
echo [OK] Запустить GUI.bat

echo.
echo ═══════════════════════════════════════════════════════════════
echo [OK] Дистрибутив создан успешно!
echo ═══════════════════════════════════════════════════════════════
echo.
echo [*] Папка: %DIST_DIR%\
echo.

REM Подсчет размера
for /f "tokens=3" %%a in ('dir "%DIST_DIR%" /s /-c ^| findstr /C:"bytes"') do set "SIZE=%%a"
set /a SIZE_MB=%SIZE%/1048576
echo [*] Размер: %SIZE_MB% MB
echo.

REM Предложение создать архив
echo [*] Создать ZIP архив? (требуется 7-Zip или WinRAR)
echo.
choice /C YN /M "Создать архив"
if errorlevel 2 goto :skip_archive
if errorlevel 1 goto :create_archive

:create_archive
REM Попытка использовать 7-Zip
where 7z >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Создаю архив с помощью 7-Zip...
    7z a -tzip "ZapretMatrixGUI_Portable_%TIMESTAMP%.zip" "%DIST_DIR%\" >nul
    if %errorlevel% equ 0 (
        echo [OK] Архив создан: ZapretMatrixGUI_Portable_%TIMESTAMP%.zip
        goto :done
    )
)

REM Попытка использовать PowerShell
echo [*] Создаю архив с помощью PowerShell...
powershell -command "Compress-Archive -Path '%DIST_DIR%' -DestinationPath 'ZapretMatrixGUI_Portable_%TIMESTAMP%.zip' -Force"
if %errorlevel% equ 0 (
    echo [OK] Архив создан: ZapretMatrixGUI_Portable_%TIMESTAMP%.zip
    goto :done
)

echo [!] Не удалось создать архив автоматически
echo [*] Создайте архив вручную из папки: %DIST_DIR%\

:skip_archive
:done
echo.
echo ═══════════════════════════════════════════════════════════════
echo [OK] Готово!
echo ═══════════════════════════════════════════════════════════════
echo.
echo [*] Дистрибутив готов к распространению
echo [*] Все файлы в папке: %DIST_DIR%\
echo.
echo [*] Пользователям НЕ нужен Python для работы!
echo.

pause
