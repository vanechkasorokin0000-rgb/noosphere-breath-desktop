"""
Страницы техники Вима Хофа
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground
from ui.tkinter.widgets import BaseBreathingApp


class BaseWimHofPage(PageWithBackground):
    """Базовый класс для страниц Вима Хофа"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(
            self.texts.LEVEL_TITLES[level]["wim_hof"], width_ratio=0.6, y_ratio=0.05
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["description"],
            command=lambda: controller.show_frame(f"WimHof{level.capitalize()}DescriptionPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.17
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["practice"],
            command=lambda: controller.show_frame(f"WimHof{level.capitalize()}Timer"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.27
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"BreathingTechniques{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.37
        )


class BeginnerWimHofPage(BaseWimHofPage):
    """Страница техники Вима Хофа для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class AdvancedWimHofPage(BaseWimHofPage):
    """Страница техники Вима Хофа для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class BaseWimHofDescriptionPage(PageWithBackground):
    """Базовый класс для страниц описания Вима Хофа"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(
            self.texts.LEVEL_TITLES[level]["wim_hof_description"], width_ratio=0.6, y_ratio=0.03
        )
        
        if level == "beginner":
            description = self.texts.WIM_HOF_BEGINNER_DESCRIPTION
        else:
            description = self.texts.WIM_HOF_ADVANCED_DESCRIPTION
        
        self.create_scrollable_label(
            text=description,
            width_ratio=0.95, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_large"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"WimHof{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class WimHofBeginnerDescriptionPage(BaseWimHofDescriptionPage):
    """Страница описания техники Вима Хофа для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class WimHofAdvancedDescriptionPage(BaseWimHofDescriptionPage):
    """Страница описания техники Вима Хофа для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class WimHofBeginnerTimer(BaseBreathingApp):
    """Таймер для Вима Хофа (начинающие)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("wim_hof", "beginner")
        super().__init__(parent, controller, bg_image, cycles, "WimHofBeginnerPage", 3, "beginner")


class WimHofAdvancedTimer(BaseBreathingApp):
    """Таймер для Вима Хофа (опытные)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("wim_hof", "advanced")
        super().__init__(parent, controller, bg_image, cycles, "WimHofAdvancedPage", 3, "advanced")
