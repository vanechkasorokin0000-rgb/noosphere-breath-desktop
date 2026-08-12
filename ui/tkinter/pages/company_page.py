"""
Страница "О проекте"
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground


class CompanyPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.TITLES["company"], y_ratio=0.03)
        
        self.create_scrollable_label(
            text=self.texts.COMPANY_DESCRIPTION,
            width_ratio=self.styles.WIDGET_SIZES["label_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["label_medium"]["height"],
            y_ratio=0.13,
            font_config=self.styles.FONTS["label_medium"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("StartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.71
        )
