#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zapret Matrix GUI - Профессиональный интерфейс в стиле Матрицы
"""

import os
import sys
import subprocess
import json
import threading
import time
from pathlib import Path
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import psutil

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class TerminalTheme:
    """Цветовая схема терминала"""
    
    # Основные цвета
    GREEN = "#00FF41"      # Яркий зелёный
    DARK = "#003B00"       # Тёмно-зелёный
    BLACK = "#000000"      # Чёрный фон
    GLOW = "#00DD00"       # Свечение
    DIM = "#006600"        # Тусклый зелёный
    
    # Акцентные цвета
    AMBER_ORANGE = "#FFA500"      # Янтарный (для предупреждений)
    DANGER_RED = "#FF4444"        # Красный (для ошибок)
    ACTIVE_CYAN = "#00FFFF"       # Cyan (для активных элементов)
    
    @staticmethod
    def get_scanline_pattern():
        """Паттерн для эффекта сканлайнов"""
        return "▓▒░"
    
    @staticmethod
    def get_border_chars():
        """Символы для рамок в стиле терминала"""
        return {
            'top_left': '╔',
            'top_right': '╗',
            'bottom_left': '╚',
            'bottom_right': '╝',
            'horizontal': '═',
            'vertical': '║'
        }


class ZapretMatrixManager:
    """Менеджер для управления Zapret"""
    
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.bin_path = self.base_path / 'bin'
        self.lists_path = self.base_path / 'lists'
        self.service_script = self.base_path / 'service.bat'
        self.config_file = self.base_path / 'zapret_matrix_config.json'
        
        self.process = None
        self.load_config()
    
    def load_config(self):
        """Загрузить конфигурацию"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = self._default_config()
        else:
            self.config = self._default_config()
    
    def _default_config(self):
        return {
            'current_strategy': 'general.bat',
            'ipset_mode': 'loaded',
            'game_filter': False,
            'auto_start': False
        }
    
    def save_config(self):
        """Сохранить конфигурацию"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def get_strategies(self):
        """Получить список стратегий"""
        strategies = []
        for file in sorted(self.base_path.glob('general*.bat')):
            strategies.append(file.name)
        return strategies
    
    def is_running(self):
        """Проверить, запущен ли zapret"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'winws.exe':
                    return True
            return False
        except:
            return False
    
    def start_strategy(self, strategy_name):
        """Запустить стратегию"""
        try:
            strategy_path = self.base_path / strategy_name
            if not strategy_path.exists():
                return False, f"Стратегия не найдена: {strategy_name}"
            
            self.process = subprocess.Popen(
                [str(strategy_path)],
                shell=True,
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.config['current_strategy'] = strategy_name
            self.save_config()
            
            time.sleep(1)  # Даём время на запуск
            
            if self.is_running():
                return True, f"Стратегия '{strategy_name}' успешно запущена"
            else:
                return False, "Процесс запустился, но winws.exe не обнаружен"
                
        except Exception as e:
            return False, f"Ошибка запуска: {str(e)}"
    
    def stop_strategy(self):
        """Остановить стратегию"""
        try:
            # Останавливаем через service.bat uninstall
            if self.service_script.exists():
                subprocess.run(
                    [str(self.service_script), 'uninstall'],
                    shell=True,
                    cwd=str(self.base_path),
                    capture_output=True,
                    timeout=10
                )
            
            # Принудительно убиваем процесс winws.exe если ещё запущен
            subprocess.run('taskkill /IM winws.exe /F', 
                         shell=True, 
                         capture_output=True,
                         timeout=5)
            
            time.sleep(0.5)
            
            if not self.is_running():
                return True, "Стратегия успешно остановлена"
            else:
                return False, "Не удалось остановить процесс"
                
        except Exception as e:
            return False, f"Ошибка остановки: {str(e)}"
    
    def get_status_info(self):
        """Получить информацию о статусе"""
        running = self.is_running()
        
        info = {
            'running': running,
            'strategy': self.config.get('current_strategy', 'N/A'),
            'ipset_mode': self.config.get('ipset_mode', 'loaded'),
            'game_filter': self.config.get('game_filter', False),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        
        return info
    
    def run_diagnostics(self):
        """Запустить диагностику"""
        try:
            subprocess.Popen(
                [str(self.service_script), 'diagnostics'],
                shell=True,
                cwd=str(self.base_path)
            )
            return True, "Диагностика запущена в отдельном окне"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def update_lists(self):
        """Обновить IP листы"""
        try:
            subprocess.Popen(
                [str(self.service_script), 'update_ipset_list'],
                shell=True,
                cwd=str(self.base_path)
            )
            return True, "Обновление IP-листов запущено"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def run_tests(self):
        """Запустить тесты"""
        try:
            subprocess.Popen(
                [str(self.service_script), 'run_tests'],
                shell=True,
                cwd=str(self.base_path)
            )
            return True, "Тесты запущены в отдельном окне"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"


class TerminalGUI:
    """Главный класс GUI"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("⚡ ZAPRET TERMINAL ⚡")
        self.root.geometry("1100x750")
        self.root.resizable(False, False)
        
        # Инициализация менеджера
        if getattr(sys, 'frozen', False):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent
        
        self.manager = ZapretMatrixManager(base_path)
        
        # Проверка наличия необходимых файлов
        if not (base_path / 'bin' / 'winws.exe').exists():
            messagebox.showerror(
                "Ошибка инициализации",
                "Не найден winws.exe в папке bin/\n\nУбедитесь, что находитесь в папке с zapret"
            )
            sys.exit(1)
        
        # Цветовая схема
        self.colors = TerminalTheme()
        
        # Настройка внешнего вида
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск обновления статуса
        self.update_status()
        
        # Запуск мигания индикаторов
        self.blink_indicator()
        
        # Центрирование окна
        self.center_window()
    
    def setup_styles(self):
        """Настройка стилей"""
        self.root.configure(fg_color=self.colors.BLACK)
        
    def blink_indicator(self):
        """Мигание индикаторов (эффект Terminal)"""
        def blink():
            if hasattr(self, 'status_indicator'):
                current_color = self.status_indicator.cget("text_color")
                if self.manager.is_running():
                    new_color = self.colors.GREEN if current_color == self.colors.GLOW else self.colors.GLOW
                    self.status_indicator.configure(text_color=new_color)
            self.root.after(800, blink)
        blink()
    
    def center_window(self):
        """Центрировать окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Создать все виджеты в стиле Terminal"""
        
        # ═══════════════════════════════════════════════════════════
        # ЗАГОЛОВОК В СТИЛЕ Terminal
        # ═══════════════════════════════════════════════════════════
        
        header_frame = ctk.CTkFrame(self.root, fg_color=self.colors.DARK, corner_radius=0, border_width=3, border_color=self.colors.GREEN)
        header_frame.pack(fill="x", pady=(0, 5))
        
        # ASCII-арт заголовок
        ascii_title = """
╔═══════════════════════════════════════════════════════════════════╗
║  ███████╗ █████╗ ██████╗ ██████╗ ███████╗████████╗              ║
║  ╚══███╔╝██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝              ║
║    ███╔╝ ███████║██████╔╝██████╔╝█████╗     ██║                 ║
║   ███╔╝  ██╔══██║██╔═══╝ ██╔══██╗██╔══╝     ██║                 ║
║  ███████╗██║  ██║██║     ██║  ██║███████╗   ██║                 ║
║  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝                 ║
║                                                                   ║
║             СИСТЕМА ОБХОДА БЛОКИРОВОК                            ║
╚═══════════════════════════════════════════════════════════════════╝
"""
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=ascii_title,
            font=("Courier New", 8, "bold"),
            text_color=self.colors.GREEN,
            justify="left"
        )
        title_label.pack(pady=5)
        
        # Основной контейнер
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # ═══════════════════════════════════════════════════════════
        # ЛЕВАЯ ПАНЕЛЬ - СТАТУС И УПРАВЛЕНИЕ
        # ═══════════════════════════════════════════════════════════
        
        left_panel = ctk.CTkFrame(main_container, fg_color=self.colors.BLACK, corner_radius=0, border_width=3, border_color=self.colors.GREEN)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # ┌─────────────────────────────────────────┐
        # │  СИСТЕМНЫЙ СТАТУС                       │
        # └─────────────────────────────────────────┘
        
        status_frame = ctk.CTkFrame(left_panel, fg_color=self.colors.DARK, corner_radius=0, border_width=2, border_color=self.colors.DIM)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        status_header = ctk.CTkLabel(
            status_frame,
            text="╔═══════════════════════════════════════════╗\n║     [[[  СИСТЕМНЫЙ СТАТУС  ]]]            ║\n╚═══════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            justify="left"
        )
        status_header.pack(pady=(8, 5))
        
        # Индикатор статуса с мигающим эффектом
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="▓▓▓ OFFLINE ▓▓▓",
            font=("Courier New", 20, "bold"),
            text_color=self.colors.DANGER_RED
        )
        self.status_indicator.pack(pady=10)
        
        # Детальная информация
        self.status_details = ctk.CTkLabel(
            status_frame,
            text="[···] Ожидание активации системы...",
            font=("Courier New", 9),
            text_color=self.colors.DIM
        )
        self.status_details.pack(pady=(0, 5))
        
        self.status_time = ctk.CTkLabel(
            status_frame,
            text="⏱ UPTIME: 00:00:00",
            font=("Courier New", 9),
            text_color=self.colors.GREEN
        )
        self.status_time.pack(pady=(0, 10))
        
        # ┌─────────────────────────────────────────┐
        # │  ВЫБОР СТРАТЕГИИ                        │
        # └─────────────────────────────────────────┘
        
        strategy_frame = ctk.CTkFrame(left_panel, fg_color=self.colors.DARK, corner_radius=0, border_width=2, border_color=self.colors.DIM)
        strategy_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        strategy_header = ctk.CTkLabel(
            strategy_frame,
            text="╔═══════════════════════════════════════════╗\n║   [[[  СТРАТЕГИЯ ОБХОДА  ]]]              ║\n╚═══════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            justify="left"
        )
        strategy_header.pack(pady=(8, 8))
        
        strategies = self.manager.get_strategies()
        current_strategy = self.manager.config.get('current_strategy', strategies[0] if strategies else '')
        
        self.strategy_var = ctk.StringVar(value=current_strategy)
        self.strategy_dropdown = ctk.CTkOptionMenu(
            strategy_frame,
            variable=self.strategy_var,
            values=strategies,
            font=("Courier New", 11, "bold"),
            fg_color=self.colors.DARK,
            button_color=self.colors.GREEN,
            button_hover_color=self.colors.GLOW,
            dropdown_fg_color=self.colors.BLACK,
            dropdown_text_color=self.colors.GREEN,
            dropdown_hover_color=self.colors.DARK
        )
        self.strategy_dropdown.pack(pady=8, padx=15, fill="x")
        
        # Кнопки управления
        buttons_container = ctk.CTkFrame(strategy_frame, fg_color="transparent")
        buttons_container.pack(pady=(5, 15))
        
        self.start_button = ctk.CTkButton(
            buttons_container,
            text="▶▶▶ АКТИВИРОВАТЬ ◀◀◀",
            command=self.start_strategy,
            font=("Courier New", 13, "bold"),
            fg_color=self.colors.GREEN,
            hover_color=self.colors.GLOW,
            text_color=self.colors.BLACK,
            width=200,
            height=45,
            corner_radius=0,
            border_width=2,
            border_color=self.colors.GLOW
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            buttons_container,
            text="■ ДЕАКТИВАЦИЯ ■",
            command=self.stop_strategy,
            font=("Courier New", 13, "bold"),
            fg_color=self.colors.DANGER_RED,
            hover_color="#CC0000",
            text_color="white",
            width=200,
            height=45,
            corner_radius=0,
            border_width=2,
            border_color="#FF6666"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # ┌─────────────────────────────────────────┐
        # │  КОНФИГУРАЦИЯ                           │
        # └─────────────────────────────────────────┘
        
        config_frame = ctk.CTkFrame(left_panel, fg_color=self.colors.DARK, corner_radius=0, border_width=2, border_color=self.colors.DIM)
        config_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        config_header = ctk.CTkLabel(
            config_frame,
            text="╔═══════════════════════════════════════════╗\n║   [[[  ПАРАМЕТРЫ СИСТЕМЫ  ]]]             ║\n╚═══════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            justify="left"
        )
        config_header.pack(pady=(8, 8))
        
        # IP фильтрация
        ip_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        ip_container.pack(pady=5, padx=15, fill="x")
        
        ip_label = ctk.CTkLabel(
            ip_container,
            text="[●] IP ФИЛЬТРАЦИЯ:",
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN
        )
        ip_label.pack(side="left", padx=(0, 10))
        
        self.ipset_var = ctk.StringVar(value=self.manager.config.get('ipset_mode', 'loaded'))
        ipset_dropdown = ctk.CTkOptionMenu(
            ip_container,
            variable=self.ipset_var,
            values=["none", "loaded", "any"],
            font=("Courier New", 10, "bold"),
            fg_color=self.colors.DARK,
            button_color=self.colors.GREEN,
            button_hover_color=self.colors.GLOW,
            command=self.update_ipset_mode,
            width=120
        )
        ipset_dropdown.pack(side="left")
        
        # Чекбоксы
        self.game_filter_var = ctk.BooleanVar(value=self.manager.config.get('game_filter', False))
        game_filter_check = ctk.CTkCheckBox(
            config_frame,
            text="[▓] ФИЛЬТР ДЛЯ ИГР (UDP/TCP)",
            variable=self.game_filter_var,
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            fg_color=self.colors.GREEN,
            hover_color=self.colors.GLOW,
            border_color=self.colors.DIM,
            command=self.update_game_filter
        )
        game_filter_check.pack(pady=8, padx=15, anchor="w")
        
        self.auto_start_var = ctk.BooleanVar(value=self.manager.config.get('auto_start', False))
        auto_start_check = ctk.CTkCheckBox(
            config_frame,
            text="[▓] АВТОЗАПУСК ПРИ СТАРТЕ",
            variable=self.auto_start_var,
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            fg_color=self.colors.GREEN,
            hover_color=self.colors.GLOW,
            border_color=self.colors.DIM,
            command=self.update_auto_start
        )
        auto_start_check.pack(pady=(0, 15), padx=15, anchor="w")
        
        # ═══════════════════════════════════════════════════════════
        # ПРАВАЯ ПАНЕЛЬ - ЛОГ И ИНФОРМАЦИЯ
        # ═══════════════════════════════════════════════════════════
        
        right_panel = ctk.CTkFrame(main_container, fg_color=self.colors.BLACK, corner_radius=0, border_width=3, border_color=self.colors.GREEN)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # ┌─────────────────────────────────────────┐
        # │  СИСТЕМНЫЙ ЖУРНАЛ                       │
        # └─────────────────────────────────────────┘
        
        log_frame = ctk.CTkFrame(right_panel, fg_color=self.colors.DARK, corner_radius=0, border_width=2, border_color=self.colors.DIM)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        log_header = ctk.CTkLabel(
            log_frame,
            text="╔═══════════════════════════════════════════╗\n║   [[[  СИСТЕМНЫЙ ЖУРНАЛ  ]]]              ║\n╚═══════════════════════════════════════════╝",
            font=("Courier New", 10, "bold"),
            text_color=self.colors.GREEN,
            justify="left"
        )
        log_header.pack(pady=(8, 5))
        
        # Создаём текстовый виджет для лога
        import tkinter as tk
        self.log_text = tk.Text(
            log_frame,
            height=25,
            width=55,
            bg=self.colors.BLACK,
            fg=self.colors.GREEN,
            font=("Courier New", 9),
            insertbackground=self.colors.GREEN,
            relief="flat",
            wrap="word",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.colors.DIM,
            highlightcolor=self.colors.GREEN
        )
        self.log_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        
        # Скроллбар для лога
        scrollbar = tk.Scrollbar(self.log_text, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Кнопки управления логом и инструменты
        log_buttons_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_buttons_frame.pack(pady=(0, 10), padx=10, fill="x")
        
        clear_log_btn = ctk.CTkButton(
            log_buttons_frame,
            text="[X] ОЧИСТИТЬ",
            command=self.clear_log,
            font=("Courier New", 10, "bold"),
            fg_color=self.colors.DARK,
            hover_color=self.colors.DIM,
            text_color=self.colors.GREEN,
            height=30,
            width=120,
            corner_radius=0,
            border_width=1,
            border_color=self.colors.GREEN
        )
        clear_log_btn.pack(side="left", padx=2)
        
        check_status_btn = ctk.CTkButton(
            log_buttons_frame,
            text="[?] СТАТУС",
            command=self.check_status,
            font=("Courier New", 10, "bold"),
            fg_color=self.colors.DARK,
            hover_color=self.colors.DIM,
            text_color=self.colors.GREEN,
            height=30,
            width=120,
            corner_radius=0,
            border_width=1,
            border_color=self.colors.GREEN
        )
        check_status_btn.pack(side="left", padx=2)
        
        open_folder_btn = ctk.CTkButton(
            log_buttons_frame,
            text="[📁] ПАПКА",
            command=self.open_folder,
            font=("Courier New", 10, "bold"),
            fg_color=self.colors.DARK,
            hover_color=self.colors.DIM,
            text_color=self.colors.GREEN,
            height=30,
            width=120,
            corner_radius=0,
            border_width=1,
            border_color=self.colors.GREEN
        )
        open_folder_btn.pack(side="left", padx=2)
        
        # Приветственное сообщение
        self.log_message("╔═══════════════════════════════════════════════════╗", "system")
        self.log_message("║        СИСТЕМА ИНИЦИАЛИЗИРОВАНА                  ║", "system")
        self.log_message("╚═══════════════════════════════════════════════════╝", "system")
        self.log_message("", "info")
        self.log_message(f"[SYS] Путь установки: {self.manager.base_path}", "info")
        self.log_message(f"[SYS] Обнаружено стратегий: {len(strategies)}", "info")
        self.log_message(f"[SYS] Режим IP: {self.manager.config.get('ipset_mode', 'N/A')}", "info")
        self.log_message("", "info")
        self.log_message("[>>>] Система готова к работе", "success")
    
    def log_message(self, message, msg_type="info"):
        """Добавить сообщение в лог (Terminal стиль)"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Определяем префикс и цвет по типу
        if msg_type == "system":
            # Системные сообщения без префикса и временной метки
            log_line = f"{message}\n"
            self.log_text.insert("end", log_line)
        else:
            prefix_map = {
                "success": "[OK]",
                "error": "[ER]",
                "info": "[>>]",
                "warning": "[!!]"
            }
            prefix = prefix_map.get(msg_type, "[>>]")
            log_line = f"[{timestamp}] {prefix} {message}\n"
            self.log_text.insert("end", log_line)
        
        self.log_text.see("end")
        self.log_text.update()
    
    def clear_log(self):
        """Очистить лог"""
        self.log_text.delete("1.0", "end")
        self.log_message("Лог очищен", "info")
    
    def update_status(self):
        """Обновить статус (Terminal стиль)"""
        def update():
            status_info = self.manager.get_status_info()
            
            if status_info['running']:
                self.status_indicator.configure(
                    text="[•] СИСТЕМА АКТИВНА",
                    text_color=self.colors.GREEN
                )
                # Запустить мигание индикатора
                if not hasattr(self, 'blinking'):
                    self.blinking = True
                    self.blink_indicator()
            else:
                self.status_indicator.configure(
                    text="[○] СИСТЕМА ОТКЛЮЧЕНА",
                    text_color=self.colors.DANGER_RED
                )
                # Остановить мигание
                self.blinking = False
            
            # Повторить через 2 секунды
            self.root.after(2000, update)
        
        update()
    
    def blink_indicator(self):
        """Мигающий эффект для активного индикатора"""
        if hasattr(self, 'blinking') and self.blinking:
            status_info = self.manager.get_status_info()
            if status_info['running']:
                # Переключить между ярким и тусклым зеленым
                current_color = self.status_indicator.cget("text_color")
                if current_color == self.colors.GREEN:
                    self.status_indicator.configure(text_color=self.colors.ACTIVE_CYAN)
                else:
                    self.status_indicator.configure(text_color=self.colors.GREEN)
                
                # Повторить через 800ms для эффекта мигания
                self.root.after(800, self.blink_indicator)
    
    def start_strategy(self):
        """Запустить стратегию (Terminal стиль)"""
        strategy = self.strategy_var.get()
        if not strategy:
            self.log_message("[!!] ОШИБКА: Выберите стратегию", "error")
            return
        
        self.start_button.configure(state="disabled")
        self.log_message("", "system")
        self.log_message("╔═══════════════════════════════════════════════════╗", "system")
        self.log_message("║            ИНИЦИАЛИЗАЦИЯ ПРОТОКОЛА DPI           ║", "system")
        self.log_message("╚═══════════════════════════════════════════════════╝", "system")
        self.log_message(f"[>>] Загрузка стратегии: {strategy}", "info")
        
        def run():
            success, message = self.manager.start_strategy(strategy)
            
            self.root.after(0, lambda: self.log_message(
                f"[{'OK' if success else 'ER'}] {message}",
                "success" if success else "error"
            ))
            self.root.after(0, lambda: self.start_button.configure(state="normal"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def stop_strategy(self):
        """Остановить стратегию (Terminal стиль)"""
        self.stop_button.configure(state="disabled")
        self.log_message("", "system")
        self.log_message("[>>] Остановка системы...", "warning")
        
        def run():
            success, message = self.manager.stop_strategy()
            
            self.root.after(0, lambda: self.log_message(
                f"[{'OK' if success else 'ER'}] {message}",
                "success" if success else "error"
            ))
            self.root.after(0, lambda: self.stop_button.configure(state="normal"))
        
        threading.Thread(target=run, daemon=True).start()
    
    def update_ipset_mode(self, value):
        """Обновить режим ipset"""
        self.manager.config['ipset_mode'] = value
        self.manager.save_config()
        self.log_message(f"Режим IP изменён на: {value}", "success")
    
    def update_game_filter(self):
        """Обновить фильтр для игр"""
        value = self.game_filter_var.get()
        self.manager.config['game_filter'] = value
        self.manager.save_config()
        status = "включен" if value else "выключен"
        self.log_message(f"Фильтр для игр {status}", "success")
    
    def update_auto_start(self):
        """Обновить автозапуск"""
        value = self.auto_start_var.get()
        self.manager.config['auto_start'] = value
        self.manager.save_config()
        status = "включен" if value else "выключен"
        self.log_message(f"Автозапуск {status}", "success")
    
    def check_status(self):
        """Проверить статус (Terminal стиль)"""
        self.log_message("", "system")
        self.log_message("╔═══════════════════════════════════════════════════╗", "system")
        self.log_message("║                ДИАГНОСТИКА СИСТЕМЫ                ║", "system")
        self.log_message("╚═══════════════════════════════════════════════════╝", "system")
        
        status_info = self.manager.get_status_info()
        
        # Статус работы
        status_text = "АКТИВНА" if status_info['running'] else "ОТКЛЮЧЕНА"
        status_icon = "[•]" if status_info['running'] else "[○]"
        self.log_message(f"{status_icon} Статус системы: {status_text}", 
                        "success" if status_info['running'] else "error")
        
        # Текущая стратегия
        strategy_text = status_info['strategy'] if status_info['strategy'] else "НЕ ВЫБРАНА"
        self.log_message(f"[>] Стратегия: {strategy_text}", "info")
        
        # Режим IP
        ipset_text = status_info['ipset_mode'].upper()
        self.log_message(f"[>] Режим IP: {ipset_text}", "info")
        
        # Фильтр игр
        game_filter_text = "ВКЛЮЧЕН" if status_info['game_filter'] else "ВЫКЛЮЧЕН"
        self.log_message(f"[>] Фильтр игр: {game_filter_text}", "info")
        
        self.log_message("", "system")
        self.log_message("[>>>] Диагностика завершена", "success")
    
    def open_folder(self):
        """Открыть папку проекта (Terminal стиль)"""
        try:
            os.startfile(str(self.manager.base_path))
            self.log_message("[>>>] Папка открыта в проводнике", "success")
        except Exception as e:
            self.log_message(f"[ER] Ошибка открытия: {str(e)}", "error")
    
    def run(self):
        """Запустить приложение"""
        self.root.mainloop()


def main():
    """Главная функция"""
    try:
        app = TerminalGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение:\n{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()

