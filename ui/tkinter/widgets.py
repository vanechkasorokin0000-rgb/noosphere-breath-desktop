"""
Кастомные виджеты для Tkinter интерфейса
"""

import tkinter as tk
import pygame
import random
import os
import sys
from PIL import Image, ImageTk
from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from core.app_controller import AppController

from .base_page import PageWithBackground
from .styles import styles


class BaseBreathingApp(tk.Frame):
    """Базовый класс для всех дыхательных практик (таймеров)"""
    
    # ==================== КОНФИГУРАЦИЯ ТАЙМЕРА ====================
    # Настройки, которые можно менять:
    
    # Текст команды (stage_text)
    STAGE_TEXT_FONT_FAMILY = "Times"
    STAGE_TEXT_FONT_SIZE = 48
    STAGE_TEXT_FONT_WEIGHT = "bold"
    STAGE_TEXT_COLOR = "white"
    STAGE_TEXT_RELX = 0.5
    STAGE_TEXT_RELY_SINGLE = 0.2       # Позиция по вертикали для одной строки
    STAGE_TEXT_RELY_DOUBLE = 0.17      # Позиция по вертикали когда есть время
    
    # Текст времени (time_text)
    TIME_TEXT_FONT_FAMILY = "Times"
    TIME_TEXT_FONT_SIZE = 48
    TIME_TEXT_FONT_WEIGHT = "bold"
    TIME_TEXT_COLOR = "white"
    TIME_TEXT_RELX = 0.5
    TIME_TEXT_RELY = 0.22              # Позиция по вертикали
    
    # Шрифт кнопок
    BUTTON_FONT_FAMILY = "Times"
    BUTTON_FONT_SIZE = 36
    BUTTON_FONT_WEIGHT = "normal"
    BUTTON_FONT_SCALE = True           # Масштабировать с окном
    BUTTON_FONT_MIN_SIZE = 16
    BUTTON_FONT_MAX_SIZE = 32
    
    # Кнопка Старт / Начать заново
    START_BUTTON_RELX = 0.5
    START_BUTTON_RELY = 0.3
    START_BUTTON_RELWIDTH = 0.2
    START_BUTTON_RELHEIGHT = 0.05
    START_BUTTON_BG_COLOR = "#F0FFFF"
    START_BUTTON_FG_COLOR = "black"
    
    # Кнопка Пауза / Продолжить
    PAUSE_BUTTON_RELX = 0.5
    PAUSE_BUTTON_RELY = 0.3
    PAUSE_BUTTON_RELWIDTH = 0.2
    PAUSE_BUTTON_RELHEIGHT = 0.05
    PAUSE_BUTTON_BG_COLOR = "#F0FFFF"
    PAUSE_BUTTON_FG_COLOR = "black"
    
    # Кнопка Закончить
    BACK_BUTTON_RELX = 0.5
    BACK_BUTTON_RELY = 0.4
    BACK_BUTTON_RELWIDTH = 0.2
    BACK_BUTTON_RELHEIGHT = 0.05
    BACK_BUTTON_BG_COLOR = "#F0FFFF"
    BACK_BUTTON_FG_COLOR = "black"
    
    # Метка с раундами
    ROUND_LABEL_FONT_FAMILY = "Arial"
    ROUND_LABEL_FONT_SIZE = 20
    ROUND_LABEL_RELX = 0.5
    ROUND_LABEL_RELY = 0.5
    ROUND_LABEL_COLOR = "white"
    # ============================================================
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image,
                 cycles: Dict[int, List[Tuple[str, int]]], back_page_name: str,
                 total_rounds: int = 10, level: str = "advanced"):
        super().__init__(parent)
        self.controller = controller
        self.bg_image = bg_image
        self.back_page_name = back_page_name
        self.total_rounds = total_rounds
        self.level = level
        self.texts = controller.get_texts()
        self.styles = styles
        
        # Применяем множитель длительности для уровня
        self.round_cycles = cycles
        
        self.config(bg=self.styles.COLORS["canvas_bg"])
        
        # Пути к ресурсам
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        self.resource_dir = os.path.join(base_path, "resources")
        
        # Загрузка ВСЕХ доступных звуков и изображений для рандомайзера
        self.all_alarm_sounds = self._load_all_sounds(["alarm1.mp3", "alarm2.mp3"])
        self.all_cycle_sounds = self._load_all_sounds(["cycle1.mp3", "cycle2.mp3", "cycle3.mp3", "cycle4.mp3"])
        self.all_background_images = self._load_all_images(["background1.jpg", "background2.jpg", "background3.jpg", "background4.jpg"])
        
        # Переменные состояния
        self.time_left = 0
        self.round_number = 1
        self.cycle_number = 1
        self.timer_active = False
        self.paused = False
        self.current_stage_message = ""
        self.stages = []
        self.original_stages = []
        self.timer_job = None
        self.is_preview_phase = False
        self.current_preview_stage = None
        
        # Флаг: был ли текущий этап уже в процессе выполнения до паузы
        self.stage_was_in_progress = False
        
        # Звуки (будут выбраны случайно при старте)
        self.current_alarm_sound = None
        self.current_cycle_sound = None
        
        # Каналы звука
        self.cycle_channel = pygame.mixer.Channel(0)
        self.alarm_channel = pygame.mixer.Channel(1)
        
        # UI
        self.widgets = []
        self._setup_ui()
    
    def _get_button_font_config(self) -> Dict:
        """Получение конфигурации шрифта для кнопок"""
        return {
            "family": self.BUTTON_FONT_FAMILY,
            "size": self.BUTTON_FONT_SIZE,
            "weight": self.BUTTON_FONT_WEIGHT,
            "scale_with_window": self.BUTTON_FONT_SCALE,
            "min_size": self.BUTTON_FONT_MIN_SIZE,
            "max_size": self.BUTTON_FONT_MAX_SIZE
        }
    

    
    def _load_all_sounds(self, filenames: List[str]) -> List[str]:
        """Загрузка всех доступных звуковых файлов"""
        sounds = []
        for fname in filenames:
            path = os.path.join(self.resource_dir, fname)
            if os.path.exists(path):
                sounds.append(path)
        return sounds
    
    def _load_all_images(self, filenames: List[str]) -> List[str]:
        """Загрузка всех доступных фоновых изображений"""
        images = []
        for fname in filenames:
            path = os.path.join(self.resource_dir, fname)
            if os.path.exists(path):
                images.append(path)
        return images
    
    def _select_random_alarm(self):
        """Случайный выбор звука сигнала"""
        if self.all_alarm_sounds:
            self.current_alarm_sound = random.choice(self.all_alarm_sounds)
        else:
            self.current_alarm_sound = None
    
    def _select_random_cycle(self):
        """Случайный выбор фонового звука"""
        if self.all_cycle_sounds:
            self.current_cycle_sound = random.choice(self.all_cycle_sounds)
        else:
            self.current_cycle_sound = None
    
    def _select_random_background(self):
        """Случайный выбор фонового изображения"""
        if self.all_background_images:
            selected = random.choice(self.all_background_images)
            return selected
        return None
    
    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.canvas = tk.Canvas(self, bg=self.styles.COLORS["canvas_bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)
        
        # Случайный выбор фона при старте
        bg_path = self._select_random_background()
        if bg_path:
            self.original_image = Image.open(bg_path)
        elif self.all_background_images:
            self.original_image = Image.open(self.all_background_images[0])
        else:
            self.original_image = None
        
        # ===== ТЕКСТ КОМАНДЫ =====
        timer_font = (self.STAGE_TEXT_FONT_FAMILY, self.STAGE_TEXT_FONT_SIZE, self.STAGE_TEXT_FONT_WEIGHT)
        
        self.stage_text = self.canvas.create_text(
            0, 0,
            text=self.texts.TIMER_MESSAGES["ready"],
            font=timer_font,
            fill=self.STAGE_TEXT_COLOR,
            anchor="center"
        )
        
        # ===== ТЕКСТ ВРЕМЕНИ =====
        self.time_text = self.canvas.create_text(
            0, 0,
            text="",
            font=timer_font,
            fill=self.TIME_TEXT_COLOR,
            anchor="center"
        )
        
        # ===== КНОПКИ (используют конфигурацию шрифта из класса) =====
        button_font_config = self._get_button_font_config()
        button_font = self._calculate_scaled_font(button_font_config)
        
        # Кнопка Старт
        self.start_button = tk.Button(
            self.canvas, text=self.texts.BUTTON_TEXTS["start_practice"],
            font=button_font, bg=self.START_BUTTON_BG_COLOR, fg=self.START_BUTTON_FG_COLOR,
            command=self._start_cycle
        )
        self.start_button.font_config = button_font_config
        self.start_button.place(
            relx=self.START_BUTTON_RELX, rely=self.START_BUTTON_RELY,
            anchor="center", relwidth=self.START_BUTTON_RELWIDTH, relheight=self.START_BUTTON_RELHEIGHT
        )
        self.widgets.append(self.start_button)
        
        # Кнопка Пауза
        self.pause_button = tk.Button(
            self.canvas, text=self.texts.BUTTON_TEXTS["pause"],
            font=button_font, bg=self.PAUSE_BUTTON_BG_COLOR, fg=self.PAUSE_BUTTON_FG_COLOR,
            command=self._toggle_pause
        )
        self.pause_button.font_config = button_font_config
        self.pause_button.place(
            relx=self.PAUSE_BUTTON_RELX, rely=self.PAUSE_BUTTON_RELY,
            anchor="center", relwidth=self.PAUSE_BUTTON_RELWIDTH, relheight=self.PAUSE_BUTTON_RELHEIGHT
        )
        self.pause_button.lower()
        self.widgets.append(self.pause_button)
        
        # Кнопка Закончить
        self.back_button = tk.Button(
            self.canvas, text=self.texts.BUTTON_TEXTS["finish"],
            font=button_font, bg=self.BACK_BUTTON_BG_COLOR, fg=self.BACK_BUTTON_FG_COLOR,
            command=self._go_back
        )
        self.back_button.font_config = button_font_config
        self.back_button.place(
            relx=self.BACK_BUTTON_RELX, rely=self.BACK_BUTTON_RELY,
            anchor="center", relwidth=self.BACK_BUTTON_RELWIDTH, relheight=self.BACK_BUTTON_RELHEIGHT
        )
        self.widgets.append(self.back_button)
        
        # ===== МЕТКА С РАУНДАМИ =====
        self.round_label_text = self.canvas.create_text(
            0, 0,
            text="",
            font=(self.ROUND_LABEL_FONT_FAMILY, self.ROUND_LABEL_FONT_SIZE),
            fill=self.ROUND_LABEL_COLOR,
            anchor="center"
        )
        
        self.update_idletasks()
        self._update_background()
        self._update_timer_labels_position()
        self._update_round_label_position()
    
    def _update_timer_labels_position(self, y_ratio_stage: float = None, y_ratio_time: float = None):
        """Обновление позиции текста команды и времени"""
        if y_ratio_stage is None:
            y_ratio_stage = self.STAGE_TEXT_RELY_DOUBLE
        if y_ratio_time is None:
            y_ratio_time = self.TIME_TEXT_RELY
            
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width > 1 and height > 1:
            x_stage = width * self.STAGE_TEXT_RELX
            x_time = width * self.TIME_TEXT_RELX
            self.canvas.coords(self.stage_text, x_stage, height * y_ratio_stage)
            self.canvas.coords(self.time_text, x_time, height * y_ratio_time)
    
    def _update_round_label_position(self):
        """Обновление позиции метки с раундами"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width > 1 and height > 1:
            x = width * self.ROUND_LABEL_RELX
            y = height * self.ROUND_LABEL_RELY
            self.canvas.coords(self.round_label_text, x, y)
    
    def _calculate_scaled_font(self, font_config: Dict) -> tuple:
        """Расчет масштабированного шрифта"""
        if not font_config.get("scale_with_window", True):
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        
        if current_width <= 1 or current_height <= 1:
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        scale_factor = min(
            current_width / self.styles.BASE_WINDOW_WIDTH,
            current_height / self.styles.BASE_WINDOW_HEIGHT
        )
        
        base_size = font_config["size"]
        scaled_size = int(base_size * scale_factor)
        min_size = font_config.get("min_size", base_size // 2)
        max_size = font_config.get("max_size", base_size * 2)
        final_size = max(min_size, min(scaled_size, max_size))
        
        return (font_config["family"], final_size, font_config.get("weight", "normal"))
    
    def _update_background(self):
        """Обновление фонового изображения"""
        if hasattr(self, 'original_image') and self.original_image:
            width = self.winfo_width()
            height = self.winfo_height()
            if width > 1 and height > 1:
                resized = self.original_image.resize((width, height), Image.LANCZOS)
                self.background_image = ImageTk.PhotoImage(resized)
                self.canvas.delete("background")
                self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")
                self.canvas.tag_lower("background")
                self._update_timer_labels_position()
                self._update_round_label_position()
    
    def _on_resize(self, event):
        """Обработка изменения размера окна"""
        if not self.canvas.winfo_exists():
            return
        
        self._update_background()
        self._update_timer_labels_position()
        self._update_round_label_position()
        
        for widget in self.widgets:
            if widget.winfo_exists() and hasattr(widget, 'font_config'):
                try:
                    new_font = self._calculate_scaled_font(widget.font_config)
                    widget.config(font=new_font)
                except tk.TclError:
                    pass
    
    def _play_sound(self, sound_path: str, channel, loop: bool = False):
        """Воспроизведение звука"""
        try:
            sound = pygame.mixer.Sound(sound_path)
            channel.play(sound, loops=-1 if loop else 0)
        except Exception as e:
            print(f"Ошибка звука: {e}")
    
    def _play_alarm(self):
        """Воспроизведение выбранного звука сигнала"""
        if self.current_alarm_sound:
            self._play_sound(self.current_alarm_sound, self.alarm_channel, loop=False)
    
    def _stop_all_sounds(self):
        """Остановка всех звуков"""
        self.cycle_channel.stop()
        self.alarm_channel.stop()
    
    def _start_cycle(self):
        """Запуск цикла практики"""
        self.timer_active = True
        self.start_button.lower()
        self.pause_button.lift()
        
        self.round_number = 1
        self.cycle_number = 1
        self.stage_was_in_progress = False
        
        self._update_round_label()
        
        self._select_random_alarm()
        self._select_random_cycle()
        
        if self.current_cycle_sound:
            self._play_sound(self.current_cycle_sound, self.cycle_channel, loop=True)
        
        self.original_stages = self.round_cycles.get(1, []).copy()
        self.stages = self.original_stages.copy()
        
        self._start_preview_phase()
    
    def _update_round_label(self):
        """Обновление метки с номером раунда"""
        round_word = self.texts.TIMER_MESSAGES.get("round", "Раунд")
        self.canvas.itemconfig(
            self.round_label_text, 
            text=f"{round_word} {self.round_number}/{self.total_rounds}"
        )
    
    def _start_preview_phase(self):
        """Начало фазы предпросмотра"""
        if self.stages and self.timer_active:
            self.current_preview_stage = self.stages[0]
            stage_message, duration = self.current_preview_stage
            
            self.is_preview_phase = True
            self.current_stage_message = stage_message
            self.stage_was_in_progress = False
            self.canvas.itemconfig(self.stage_text, text=stage_message)
            self.canvas.itemconfig(self.time_text, text="")
            self._update_timer_labels_position(y_ratio_stage=self.STAGE_TEXT_RELY_SINGLE)
            
            self._play_alarm()
            
            self.time_left = 1
            self._update_timer(self._start_main_phase)
        else:
            self._complete_round()
    
    def _start_main_phase(self):
        """Начало основной фазы"""
        if self.stages and self.timer_active:
            stage_message, duration = self.stages.pop(0)
            
            self.is_preview_phase = False
            self.current_stage_message = stage_message
            self.time_left = duration
            self.stage_was_in_progress = True
            
            self._update_timer(self._start_preview_phase)
        else:
            self._complete_round()
    
    def _go_back(self):
        """Возврат на предыдущую страницу"""
        self._stop_all_sounds()
        if self.timer_job:
            self.after_cancel(self.timer_job)
        self.controller.show_frame(self.back_page_name)
    
    def _toggle_pause(self):
        """Пауза/возобновление"""
        if self.timer_active:
            self._pause_timer()
        else:
            self._resume_timer()
    
    def _pause_timer(self):
        """Пауза таймера"""
        self.timer_active = False
        self.paused = True
        self.pause_button.config(text=self.texts.BUTTON_TEXTS["resume"])
    
    def _resume_timer(self):
        """Возобновление таймера"""
        if self.paused:
            self.timer_active = True
            self.paused = False
            self.pause_button.config(text=self.texts.BUTTON_TEXTS["pause"])
            
            if self.stage_was_in_progress:
                self.is_preview_phase = False
                minutes, seconds = divmod(self.time_left, 60)
                self.canvas.itemconfig(self.stage_text, text=self.current_stage_message)
                self.canvas.itemconfig(self.time_text, text=f"{minutes:02}:{seconds:02}")
                self._update_timer_labels_position()
                self._update_timer(self._start_preview_phase)
            else:
                if self.stages:
                    self.current_preview_stage = self.stages[0]
                    stage_message, duration = self.current_preview_stage
                    
                    self.is_preview_phase = True
                    self.current_stage_message = stage_message
                    self.canvas.itemconfig(self.stage_text, text=stage_message)
                    self.canvas.itemconfig(self.time_text, text="")
                    self._update_timer_labels_position(y_ratio_stage=self.STAGE_TEXT_RELY_SINGLE)
                    
                    self._play_alarm()
                    
                    self.time_left = 1
                    self._update_timer(self._start_main_phase)
                else:
                    self._complete_round()
    
    def _get_next_phase(self):
        """Получение следующей фазы"""
        if self.is_preview_phase:
            return self._start_preview_phase
        elif self.stages:
            return self._start_main_phase
        else:
            return self._complete_round
    
    def _update_timer(self, next_phase):
        """Обновление таймера"""
        if self.time_left > 0 and self.timer_active and not self.paused:
            if self.is_preview_phase:
                self.canvas.itemconfig(self.stage_text, text=self.current_stage_message)
                self.canvas.itemconfig(self.time_text, text="")
                self._update_timer_labels_position(y_ratio_stage=self.STAGE_TEXT_RELY_SINGLE)
            else:
                minutes, seconds = divmod(self.time_left, 60)
                self.canvas.itemconfig(self.stage_text, text=self.current_stage_message)
                self.canvas.itemconfig(self.time_text, text=f"{minutes:02}:{seconds:02}")
                self._update_timer_labels_position()
            
            self.time_left -= 1
            self.timer_job = self.after(1000, lambda: self._update_timer(next_phase))
        elif self.time_left == 0 and self.timer_active and not self.paused:
            if not self.is_preview_phase:
                self.alarm_channel.stop()
            
            if next_phase:
                next_phase()
    
    def _complete_round(self):
        """Завершение раунда"""
        self.round_number += 1
        if self.round_number <= self.total_rounds:
            self.cycle_number += 1
            self.original_stages = self.round_cycles.get(self.cycle_number, self.round_cycles.get(1, [])).copy()
            self.stages = self.original_stages.copy()
            self.stage_was_in_progress = False
            self._update_round_label()
            self._start_preview_phase()
        else:
            self._complete_cycles()
    
    def _complete_cycles(self):
        """Завершение всех циклов"""
        self.timer_active = False
        self.cycle_channel.stop()
        self.alarm_channel.stop()
        self.canvas.itemconfig(self.stage_text, text=self.texts.TIMER_MESSAGES["completed"])
        self.canvas.itemconfig(self.time_text, text="")
        self._update_timer_labels_position(y_ratio_stage=self.STAGE_TEXT_RELY_SINGLE)
        self.start_button.lift()
        self.pause_button.lower()
        self.start_button.config(text=self.texts.BUTTON_TEXTS["restart"], command=self._restart_cycle)
        self.canvas.itemconfig(self.round_label_text, text="")
    
    def _restart_cycle(self):
        """Перезапуск практики"""
        self._stop_all_sounds()
        if self.timer_job:
            self.after_cancel(self.timer_job)
        
        self.time_left = 0
        self.round_number = 1
        self.cycle_number = 1
        self.timer_active = False
        self.paused = False
        self.is_preview_phase = False
        self.current_preview_stage = None
        self.stage_was_in_progress = False
        self.canvas.itemconfig(self.stage_text, text=self.texts.TIMER_MESSAGES["ready"])
        self.canvas.itemconfig(self.time_text, text="")
        self._update_timer_labels_position(y_ratio_stage=self.STAGE_TEXT_RELY_SINGLE)
        self.start_button.config(text=self.texts.BUTTON_TEXTS["start_practice"], command=self._start_cycle)
        self._start_cycle()
    
    def destroy(self):
        """Очистка ресурсов при уничтожении"""
        self._stop_all_sounds()
        if self.timer_job:
            self.after_cancel(self.timer_job)
        super().destroy()
