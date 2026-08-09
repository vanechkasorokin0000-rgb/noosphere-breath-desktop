"""
Страницы других техник (борьба с зависимостями и т.д.)
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground
from ui.tkinter.widgets import BaseBreathingApp


class OtherTechniquesMainPage(PageWithBackground):
    """Главная страница других техник"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.TITLES["other_techniques_main"], y_ratio=0.05)
        
        self.create_scrollable_label(
            text=self.texts.OTHER_TECHNIQUES_MAIN_DESCRIPTION,
            width_ratio=0.8, height_ratio=0.3, y_ratio=0.15,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["description"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["addiction_battle"],
            command=lambda: controller.show_frame("AddictionBattleTechniquePage"),
            width_ratio=0.4, height_ratio=0.06, y_ratio=0.50,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("BreathingTechniquesPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.60,
            font_config=self.styles.FONTS["button"]
        )


class AddictionBattleTechniquePage(PageWithBackground):
    """Страница техники для борьбы с зависимостями"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.TITLES["addiction_battle_technique"], width_ratio=0.6, y_ratio=0.05)
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["description"],
            command=lambda: controller.show_frame("AddictionBattleDescriptionPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.17
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["practice"],
            command=lambda: controller.show_frame("AddictionBattleTimerApp"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.27
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("OtherTechniquesMainPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.37
        )


class AddictionBattleDescriptionPage(PageWithBackground):
    """Страница описания техники для борьбы с зависимостями"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.TITLES["addiction_battle_description"], width_ratio=0.7, y_ratio=0.03)
        
        self.create_scrollable_label(
            text=self.texts.ADDICTION_BATTLE_DESCRIPTION,
            width_ratio=0.95, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_large"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("AddictionBattleTechniquePage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class AddictionBattleTimerApp(BaseBreathingApp):
    """Таймер для техники борьбы с зависимостями"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("addiction", "advanced")
        super().__init__(parent, controller, bg_image, cycles, "AddictionBattleTechniquePage", 3, "advanced")
