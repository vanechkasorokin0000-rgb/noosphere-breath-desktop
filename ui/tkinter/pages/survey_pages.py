"""
Страницы опросника
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground


class SurveyStartPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(
            self.texts.TITLES.get("survey_start", "Опросник дыхательных практик"),
            y_ratio=0.03, width_ratio=0.5, height_ratio=0.08
        )
        
        self.create_scrollable_label(
            text=self.texts.SURVEY_START_DESCRIPTION,
            width_ratio=0.8, height_ratio=0.5, y_ratio=0.13,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["description"],
            justify="center"  # Добавлено
        )
        
        self.create_button(
            text=self.texts.SURVEY_START_BUTTON,
            command=lambda: controller.show_frame("SurveyQuestion_1"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.67,
            font_config=self.styles.SURVEY_FONTS["option_button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("StartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.75,
            font_config=self.styles.SURVEY_FONTS["option_button"]
        )


class SurveyQuestionPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, question_index: int = 0):
        super().__init__(parent, controller, bg_image)
        
        self.question_index = question_index
        
        total_questions = self.controller.get_survey_questions_count()
        
        self.create_title(
            f"{self.texts.SURVEY_QUESTION_TITLE} {question_index + 1} {self.texts.SURVEY_OF_TEXT} {total_questions}",
            y_ratio=0.03
        )
        
        question = self.controller.get_survey_question(question_index)
        
        self.create_rounded_label(
            text=question["text"],
            width_ratio=0.9, height_ratio=0.08, y_ratio=0.13,
            bg_color=self.styles.SURVEY_COLORS["label_bg"],
            font_config=self.styles.SURVEY_FONTS["question"],
            border_radius=self.styles.SURVEY_BORDER_RADIUS
        )
        
        self.create_rounded_label(
            text=question["description"],
            width_ratio=0.9, height_ratio=0.08, y_ratio=0.23,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["description"],
            border_radius=self.styles.SURVEY_BORDER_RADIUS
        )
        
        self._create_options(question["options"])
    
    def _create_options(self, options: list):
        y_start = self.styles.SURVEY_CONFIG["options_y_start"]
        
        for i, option in enumerate(options):
            y_pos = y_start + i * self.styles.SURVEY_CONFIG["option_y_step"]
            
            self.create_button(
                text=option["text"],
                command=lambda v=option["value"], opt_text=option["text"]: self._select_answer(v),
                width_ratio=self.styles.SURVEY_CONFIG["option_button_width"],
                height_ratio=self.styles.SURVEY_CONFIG["option_button_height"],
                y_ratio=y_pos,
                font_config=self.styles.SURVEY_FONTS["option_button"]
            )
            
            self.create_rounded_label(
                text=option["description"],
                width_ratio=self.styles.SURVEY_CONFIG["option_hint_width"],
                height_ratio=self.styles.SURVEY_CONFIG["option_hint_height"],
                y_ratio=y_pos + self.styles.SURVEY_CONFIG["option_hint_y_offset"],
                x_ratio=self.styles.SURVEY_CONFIG["option_hint_x_offset"],
                bg_color=self.styles.SURVEY_COLORS["option_hint_bg"],
                font_config=self.styles.SURVEY_FONTS["option_hint"],
                border_radius=self.styles.SURVEY_BORDER_RADIUS
            )
    
    def _select_answer(self, value: str):
        """Обработка выбора ответа с проверкой существования страниц"""
        try:
            question = self.controller.get_survey_question(self.question_index)
            self.controller.save_survey_answer(question["id"], value)
            
            next_index = self.question_index + 1
            total_questions = self.controller.get_survey_questions_count()
            
            if next_index < total_questions:
                next_page = f"SurveyQuestion_{next_index + 1}"
                
                app_instance = self.controller._app_instance
                if app_instance and next_page in app_instance.page_classes:
                    self.controller.show_frame(next_page)
                else:
                    self.controller.show_frame("SurveyResultPage")
            else:
                self.controller.show_frame("SurveyResultPage")
                
        except Exception as e:
            print(f"Ошибка при обработке ответа: {e}")
            import traceback
            traceback.print_exc()
            self.controller.show_frame("StartPage")


class SurveyResultPage(PageWithBackground):
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        result = self.controller.get_survey_result()
        
        self.create_title(result["title"], width_ratio=0.6, height_ratio=0.08, y_ratio=0.03)
        
        self.create_scrollable_label(
            text=result["description"],
            width_ratio=0.9, height_ratio=0.48, y_ratio=0.13,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["result_text"],
            justify="center"  # Добавлено
        )
        
        if "tips" in result:
            self.create_rounded_label(
                text=result["tips"],
                width_ratio=0.85, height_ratio=0.06, y_ratio=0.63,
                bg_color=self.styles.SURVEY_COLORS["tip_bg"],
                font_config=self.styles.SURVEY_FONTS["tip"],
                border_radius=self.styles.SURVEY_BORDER_RADIUS
            )
        
        self.create_button(
            text=f"{self.texts.SURVEY_GO_TO_PRACTICE} {result['practice']}",
            command=lambda: controller.show_frame(result["page"]),
            width_ratio=0.3, height_ratio=0.05, y_ratio=0.72,
            font_config=self.styles.SURVEY_FONTS["option_button"]
        )
        
        self.create_button(
            text=self.texts.SURVEY_FINISH_BUTTON,
            command=lambda: controller.show_frame("StartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.80,
            font_config=self.styles.SURVEY_FONTS["option_button"]
        )
