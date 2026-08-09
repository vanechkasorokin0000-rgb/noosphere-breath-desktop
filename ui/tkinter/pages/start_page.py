"""
Стартовая страница приложения
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground


class StartPage(PageWithBackground):
    """Стартовая страница с кнопками навигации и переключения языка"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        print("StartPage инициализация...")
        
        self.create_title(self.texts.TITLES["start"], y_ratio=0.05)
        
        button_y_start = 0.12
        button_step = 0.08
        
        self._create_main_buttons(button_y_start, button_step)
        self._create_language_buttons()
        
        print("StartPage инициализация завершена")
    
    def _create_main_buttons(self, y_start: float, step: float):
        buttons = [
            ("survey", lambda: self.controller.show_frame("SurveyStartPage"), self.texts.BUTTON_TOOLTIPS["survey"]),
            ("diary", lambda: self.controller.show_frame("DiaryStartPage"), self.texts.BUTTON_TOOLTIPS["diary"]),
            ("about_project", lambda: self.controller.show_frame("CompanyPage"), self.texts.BUTTON_TOOLTIPS["about"]),
            ("breathing_techniques", lambda: self.controller.show_frame("BreathingTechniquesPage"), self.texts.BUTTON_TOOLTIPS["techniques"]),
            ("exit", self.controller.cleanup, self.texts.BUTTON_TOOLTIPS["exit"])
        ]
        
        for i, (key, command, tooltip) in enumerate(buttons):
            self.create_button_with_tooltip(
                text=self.texts.BUTTON_TEXTS[key],
                command=command,
                tooltip_text=tooltip,
                width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
                height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
                y_ratio=y_start + i * step
            )
    
    def _create_language_buttons(self):
        """Создание кнопок переключения языка"""
        button_width = self.styles.LANGUAGE_BUTTON_WIDTH
        gap = self.styles.LANGUAGE_BUTTON_GAP
        y_ratio = self.styles.LANGUAGE_BUTTON_Y_RATIO
        
        total_width = button_width * 2 + gap
        start_x = (1 - total_width) / 2
        
        # Кнопка "Русский"
        self.create_button(
            text="Русский",
            command=lambda: self.controller.switch_language("ru"),
            width_ratio=button_width,
            height_ratio=self.styles.LANGUAGE_BUTTON_HEIGHT,
            y_ratio=y_ratio,
            x_ratio=start_x,
            font_config=self.styles.LANGUAGE_BUTTON_FONT
        )
        
        # Кнопка "English"
        self.create_button(
            text="English",
            command=lambda: self.controller.switch_language("en"),
            width_ratio=button_width,
            height_ratio=self.styles.LANGUAGE_BUTTON_HEIGHT,
            y_ratio=y_ratio,
            x_ratio=start_x + button_width + gap,
            font_config=self.styles.LANGUAGE_BUTTON_FONT
        )
