"""
Страницы пранаям (Сама Вритти, Анулома Вилома, Брамари)
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground
from ui.tkinter.widgets import BaseBreathingApp


# ==================== ОБЩИЕ СТРАНИЦЫ ПРАНАЯМ ====================

class BasePranasPage(PageWithBackground):
    """Базовый класс для страниц выбора пранаям"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(self.texts.LEVEL_TITLES[level]["pranas"], y_ratio=0.05)
        
        buttons = [
            (self.texts.BUTTON_TEXTS["pranas_description"], f"Pranas{level.capitalize()}DescriptionPage", 0.17),
            (self.texts.BUTTON_TEXTS["sama_vritti"], f"Prana1{level.capitalize()}Page", 0.27),
            (self.texts.BUTTON_TEXTS["anuloma_viloma"], f"Prana2{level.capitalize()}Page", 0.37),
            (self.texts.BUTTON_TEXTS["brahmari"], f"Prana3{level.capitalize()}Page", 0.47),
            (self.texts.BUTTON_TEXTS["back"], f"BreathingTechniques{level.capitalize()}Page", 0.57)
        ]
        
        for text, page, y_pos in buttons:
            self.create_button(
                text=text,
                command=lambda p=page: controller.show_frame(p),
                width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
                height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
                y_ratio=y_pos
            )


class BeginnerPranasPage(BasePranasPage):
    """Страница пранаям для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class AdvancedPranasPage(BasePranasPage):
    """Страница пранаям для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class BasePranasDescriptionPage(PageWithBackground):
    """Базовый класс для страниц общего описания пранаям"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.LEVEL_TITLES[level]["pranas_description"], y_ratio=0.03)
        
        if level == "beginner":
            description = self.texts.PRANAS_BEGINNER_DESCRIPTION
        else:
            description = self.texts.PRANAS_ADVANCED_DESCRIPTION
        
        self.create_scrollable_label(
            text=description,
            width_ratio=0.9, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_medium"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Pranas{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class PranasBeginnerDescriptionPage(BasePranasDescriptionPage):
    """Страница общего описания пранаям для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class PranasAdvancedDescriptionPage(BasePranasDescriptionPage):
    """Страница общего описания пранаям для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


# ==================== СТРАНИЦЫ САМА ВРИТТИ (PRANA1) ====================

class BasePrana1Page(PageWithBackground):
    """Базовый класс для страниц Сама Вритти"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana1"], y_ratio=0.05)
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["description"],
            command=lambda: controller.show_frame(f"Prana1{level.capitalize()}DescriptionPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.17
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["practice"],
            command=lambda: controller.show_frame(f"Prana1{level.capitalize()}Timer"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.27
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Pranas{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.37
        )


class BeginnerPrana1Page(BasePrana1Page):
    """Страница Сама Вритти для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class AdvancedPrana1Page(BasePrana1Page):
    """Страница Сама Вритти для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class BasePrana1DescriptionPage(PageWithBackground):
    """Базовый класс для страниц описания Сама Вритти"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana1_description"], y_ratio=0.03)
        
        if level == "beginner":
            description = self.texts.PRANA1_BEGINNER_DESCRIPTION
        else:
            description = self.texts.PRANA1_ADVANCED_DESCRIPTION
        
        self.create_scrollable_label(
            text=description,
            width_ratio=0.95, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_medium"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Prana1{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class Prana1BeginnerDescriptionPage(BasePrana1DescriptionPage):
    """Страница описания Сама Вритти для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class Prana1AdvancedDescriptionPage(BasePrana1DescriptionPage):
    """Страница описания Сама Вритти для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class Prana1BeginnerTimer(BaseBreathingApp):
    """Таймер для Сама Вритти (начинающие)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana1", "beginner")
        super().__init__(parent, controller, bg_image, cycles, "Prana1BeginnerPage", 10, "beginner")


class Prana1AdvancedTimer(BaseBreathingApp):
    """Таймер для Сама Вритти (опытные)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana1", "advanced")
        super().__init__(parent, controller, bg_image, cycles, "Prana1AdvancedPage", 10, "advanced")


# ==================== СТРАНИЦЫ АНУЛОМА ВИЛОМА (PRANA2) ====================

class BasePrana2Page(PageWithBackground):
    """Базовый класс для страниц Анулома Вилома"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana2"], width_ratio=0.6, y_ratio=0.05)
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["description"],
            command=lambda: controller.show_frame(f"Prana2{level.capitalize()}DescriptionPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.17
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["practice"],
            command=lambda: controller.show_frame(f"Prana2{level.capitalize()}Timer"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.27
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Pranas{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.37
        )


class BeginnerPrana2Page(BasePrana2Page):
    """Страница Анулома Вилома для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class AdvancedPrana2Page(BasePrana2Page):
    """Страница Анулома Вилома для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class BasePrana2DescriptionPage(PageWithBackground):
    """Базовый класс для страниц описания Анулома Вилома"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana2_description"], y_ratio=0.03)
        
        if level == "beginner":
            description = self.texts.PRANA2_BEGINNER_DESCRIPTION
        else:
            description = self.texts.PRANA2_ADVANCED_DESCRIPTION
        
        self.create_scrollable_label(
            text=description,
            width_ratio=0.95, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_medium"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Prana2{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class Prana2BeginnerDescriptionPage(BasePrana2DescriptionPage):
    """Страница описания Анулома Вилома для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class Prana2AdvancedDescriptionPage(BasePrana2DescriptionPage):
    """Страница описания Анулома Вилома для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class Prana2BeginnerTimer(BaseBreathingApp):
    """Таймер для Анулома Вилома (начинающие)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana2", "beginner")
        super().__init__(parent, controller, bg_image, cycles, "Prana2BeginnerPage", 10, "beginner")


class Prana2AdvancedTimer(BaseBreathingApp):
    """Таймер для Анулома Вилома (опытные)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana2", "advanced")
        super().__init__(parent, controller, bg_image, cycles, "Prana2AdvancedPage", 10, "advanced")


# ==================== СТРАНИЦЫ БРАМАРИ (PRANA3) ====================

class BasePrana3Page(PageWithBackground):
    """Базовый класс для страниц Брамари"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        self.level = level
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana3"], y_ratio=0.05)
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["description"],
            command=lambda: controller.show_frame(f"Prana3{level.capitalize()}DescriptionPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.17
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["practice"],
            command=lambda: controller.show_frame(f"Prana3{level.capitalize()}Timer"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.27
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Pranas{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.37
        )


class BeginnerPrana3Page(BasePrana3Page):
    """Страница Брамари для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class AdvancedPrana3Page(BasePrana3Page):
    """Страница Брамари для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class BasePrana3DescriptionPage(PageWithBackground):
    """Базовый класс для страниц описания Брамари"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, level: str):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.LEVEL_TITLES[level]["prana3_description"], y_ratio=0.03)
        
        if level == "beginner":
            description = self.texts.PRANA3_BEGINNER_DESCRIPTION
        else:
            description = self.texts.PRANA3_ADVANCED_DESCRIPTION
        
        self.create_scrollable_label(
            text=description,
            width_ratio=0.95, height_ratio=0.65, y_ratio=0.10,
            font_config=self.styles.FONTS["label_medium"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame(f"Prana3{level.capitalize()}Page"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.78
        )


class Prana3BeginnerDescriptionPage(BasePrana3DescriptionPage):
    """Страница описания Брамари для начинающих"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "beginner")


class Prana3AdvancedDescriptionPage(BasePrana3DescriptionPage):
    """Страница описания Брамари для опытных"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image, "advanced")


class Prana3BeginnerTimer(BaseBreathingApp):
    """Таймер для Брамари (начинающие)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana3", "beginner")
        super().__init__(parent, controller, bg_image, cycles, "Prana3BeginnerPage", 7, "beginner")


class Prana3AdvancedTimer(BaseBreathingApp):
    """Таймер для Брамари (опытные)"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        cycles = controller.get_timer_cycles_for_technique("prana3", "advanced")
        super().__init__(parent, controller, bg_image, cycles, "Prana3AdvancedPage", 7, "advanced")
