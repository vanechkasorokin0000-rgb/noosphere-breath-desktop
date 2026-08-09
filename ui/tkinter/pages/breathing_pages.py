"""
Страницы выбора дыхательных техник
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground


class BreathingTechniquesPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.TITLES["breathing_techniques"], y_ratio=0.03)
        
        self.create_scrollable_label(
            text=self.texts.BREATHING_LEVELS_DESCRIPTION,
            width_ratio=0.9, height_ratio=0.35, y_ratio=0.12,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["description"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.LEVEL_BUTTONS["beginner"],
            command=lambda: controller.show_frame("BreathingTechniquesBeginnerPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=0.50,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.LEVEL_BUTTONS["advanced"],
            command=lambda: controller.show_frame("BreathingTechniquesAdvancedPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=0.58,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["other_techniques_main"],
            command=lambda: controller.show_frame("OtherTechniquesMainPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=0.66,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("StartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.74
        )


class LevelBasedTechniquesPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(
            self.texts.LEVEL_TITLES[level]["breathing_techniques"], y_ratio=0.05
        )
        
        buttons = [
            (self.texts.BUTTON_TEXTS["wim_hof"], f"WimHof{level.capitalize()}Page", 0.17),
            (self.texts.BUTTON_TEXTS["pranas"], f"Pranas{level.capitalize()}Page", 0.27),
            (self.texts.BUTTON_TEXTS["back"], "BreathingTechniquesPage", 0.37)
        ]
        
        for text, page, y_pos in buttons:
            self.create_button(
                text=text,
                command=lambda p=page: controller.show_frame(p),
                width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
                height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
                y_ratio=y_pos
            )


class BreathingTechniquesBeginnerPage(LevelBasedTechniquesPage):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class BreathingTechniquesAdvancedPage(LevelBasedTechniquesPage):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")
