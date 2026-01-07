#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для сборки Zapret Matrix GUI в standalone .exe файл
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """Проверка установки PyInstaller"""
    try:
        import PyInstaller
        print("[OK] PyInstaller установлен")
        return True
    except ImportError:
        print("[!] PyInstaller не найден")
        print("[*] Устанавливаю PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[OK] PyInstaller установлен")
            return True
        except Exception as e:
            print(f"[ERROR] Не удалось установить PyInstaller: {e}")
            return False

def clean_build_dirs():
    """Очистка директорий сборки"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"[*] Удаляю {dir_name}/")
            shutil.rmtree(dir_name, ignore_errors=True)
    
    for pattern in files_to_clean:
        for file in Path('.').glob(pattern):
            print(f"[*] Удаляю {file}")
            file.unlink()

def build_exe():
    """Сборка .exe файла"""
    print("\n" + "="*60)
    print("Zapret Matrix GUI - Сборка исполняемого файла")
    print("="*60 + "\n")
    
    # Проверка PyInstaller
    if not check_pyinstaller():
        return False
    
    # Очистка старых сборок
    print("\n[*] Очистка старых файлов сборки...")
    clean_build_dirs()
    
    # Параметры сборки PyInstaller
    pyinstaller_args = [
        'zapret_matrix_gui.py',
        '--name=ZapretMatrixGUI',
        '--onefile',  # Один файл
        '--windowed',  # Без консоли
        '--icon=NONE',  # Можно указать иконку, если есть
        '--add-data=zapret_matrix_config.json;.',
        '--add-data=lists;lists',
        '--add-data=bin;bin',
        '--add-data=service.bat;.',
        '--add-data=*.bat;.',  # Все bat файлы
        '--hidden-import=customtkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=psutil',
        '--collect-all=customtkinter',
        '--noconfirm',
        '--clean',
    ]
    
    print("\n[*] Запускаю PyInstaller...")
    print(f"[*] Команда: pyinstaller {' '.join(pyinstaller_args)}")
    print("\n[!] Это может занять несколько минут...\n")
    
    try:
        # Запуск PyInstaller
        subprocess.check_call([sys.executable, '-m', 'PyInstaller'] + pyinstaller_args)
        
        print("\n" + "="*60)
        print("[OK] Сборка завершена успешно!")
        print("="*60)
        
        # Проверка результата
        exe_path = Path('dist/ZapretMatrixGUI.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n[OK] Файл создан: {exe_path}")
            print(f"[*] Размер: {size_mb:.1f} MB")
            print(f"\n[*] Для запуска используйте: dist\\ZapretMatrixGUI.exe")
            return True
        else:
            print("\n[ERROR] Файл не найден!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Ошибка сборки: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Неожиданная ошибка: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    
    if success:
        print("\n[*] Готово! Теперь можно распространять ZapretMatrixGUI.exe")
        print("[*] Пользователям НЕ нужен Python для запуска!")
    else:
        print("\n[ERROR] Сборка не удалась")
        sys.exit(1)
    
    input("\nНажмите Enter для выхода...")
