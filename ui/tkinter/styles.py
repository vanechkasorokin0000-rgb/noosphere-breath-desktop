"""
Косметические настройки Tkinter интерфейса
Все настройки вынесены из texts.py для чистоты разделения
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class TkinterStyles:
    """
    Стили для Tkinter интерфейса
    Не зависят от языка и бизнес-логики
    """
    
    # ==================== БАЗОВЫЕ РАЗМЕРЫ ДЛЯ МАСШТАБИРОВАНИЯ ====================
    BASE_WINDOW_WIDTH: int = 1920
    BASE_WINDOW_HEIGHT: int = 1080
    
    # ==================== ОСНОВНЫЕ ШРИФТЫ ====================
    FONTS: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "title": {
            "family": "Times",
            "size": 48,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 24,
            "max_size": 56
        },
        "button": {
            "family": "Times",
            "size": 24,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 16,
            "max_size": 32
        },
        "label_title": {
            "family": "Times",
            "size": 24,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 18,
            "max_size": 30
        },
        "label_large": {
            "family": "Times",
            "size": 22,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 16,
            "max_size": 28
        },
        "label_medium": {
            "family": "Times",
            "size": 20,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 14,
            "max_size": 24
        },
        "label_small": {
            "family": "Times",
            "size": 18,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 12,
            "max_size": 22
        },
        "timer": {
            "family": "Times",
            "size": 48,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 32,
            "max_size": 64
        }
    })
    
    # ==================== РАЗМЕРЫ ВИДЖЕТОВ ====================
    WIDGET_SIZES: Dict[str, Dict[str, float]] = field(default_factory=lambda: {
        "button_small": {"width": 0.15, "height": 0.04},
        "button_medium": {"width": 0.2, "height": 0.05},
        "button_large": {"width": 0.25, "height": 0.06},
        "title": {"width": 0.35, "height": 0.07},
        "label_small": {"width": 0.7, "height": 0.5},
        "label_medium": {"width": 0.8, "height": 0.55},
        "label_large": {"width": 0.9, "height": 0.6},
        "label_full": {"width": 0.95, "height": 0.7}
    })
    
    # ==================== ЦВЕТОВАЯ СХЕМА ====================
    COLORS: Dict[str, str] = field(default_factory=lambda: {
        "title_bg": "#FFB2D0",
        "title_fg": "white",
        "button_bg": "#F0FFFF",
        "button_fg": "black",
        "button_hover_bg": "#E0EEEE",
        "label_bg": "#F0FFFF",
        "label_fg": "black",
        "canvas_bg": "#F0FFFF",
        "timer_bg": "#F0FFFF",
        "timer_fg": "black"
    })
    
    # ==================== НАСТРОЙКИ ПЕРЕНОСА ТЕКСТА ====================
    TEXT_WRAP: Dict[str, float] = field(default_factory=lambda: {
        "title": 0.95,
        "button": 0.90,
        "label": 0.95
    })
    
    # ==================== ЦВЕТА ОПРОСНИКА ====================
    SURVEY_COLORS: Dict[str, str] = field(default_factory=lambda: {
        "title_bg": "#FFB2D0",
        "title_fg": "white",
        "button_bg": "#F0FFFF",
        "button_fg": "black",
        "label_bg": "#FFF8DC",
        "label_fg": "black",
        "tip_bg": "#FAEBD7",
        "tip_fg": "black",
        "description_bg": "#FFF5EE",
        "description_fg": "black",
        "option_hint_bg": "#FFFAF0",
        "option_hint_fg": "black",
        "canvas_bg": "#F0FFFF"
    })
    
    # ==================== РАДИУС СКРУГЛЕНИЯ ====================
    SURVEY_BORDER_RADIUS: int = 20
    
    # ==================== ШРИФТЫ ОПРОСНИКА ====================
    SURVEY_FONTS: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "title": {
            "family": "Times",
            "size": 32,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 20,
            "max_size": 40
        },
        "question": {
            "family": "Times",
            "size": 28,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 18,
            "max_size": 34
        },
        "description": {
            "family": "Times",
            "size": 20,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 14,
            "max_size": 26
        },
        "option_button": {
            "family": "Times",
            "size": 20,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 14,
            "max_size": 26
        },
        "option_hint": {
            "family": "Times",
            "size": 16,
            "weight": "italic",
            "scale_with_window": True,
            "min_size": 12,
            "max_size": 20
        },
        "result_title": {
            "family": "Times",
            "size": 36,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 24,
            "max_size": 44
        },
        "result_text": {
            "family": "Times",
            "size": 22,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 16,
            "max_size": 28
        },
        "tip": {
            "family": "Times",
            "size": 18,
            "weight": "italic",
            "scale_with_window": True,
            "min_size": 14,
            "max_size": 22
        }
    })
    
    # ==================== НАСТРОЙКИ ОПРОСНИКА (ПОЗИЦИОНИРОВАНИЕ) ====================
    SURVEY_CONFIG: Dict[str, float] = field(default_factory=lambda: {
        "description_height_ratio": 0.5,
        "options_y_start": 0.35,
        "option_y_step": 0.13,
        "option_button_width": 0.5,
        "option_button_height": 0.06,
        "option_hint_width": 0.35,
        "option_hint_height": 0.04,
        "option_hint_x_offset": 0.57,
        "option_hint_y_offset": 0.06
    })
    
    # ==================== НАСТРОЙКИ ДИАЛОГОВЫХ ОКОН ====================
    DIALOG_CONFIG: Dict[str, Any] = field(default_factory=lambda: {
        "width_ratio": 0.4,
        "height_ratio": 0.3,
        "min_width": 300,
        "min_height": 200,
        "content_padding_x": 0.05,
        "content_padding_y": 0.05,
        "title_pady": 15,
        "message_pady": 10,
        "message_padx": 20,
        "button_pady": 15,
        "title_font": {
            "family": "Times",
            "size": 20,
            "weight": "bold",
            "scale_with_window": True,
            "min_size": 14,
            "max_size": 28
        },
        "message_font": {
            "family": "Times",
            "size": 16,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 12,
            "max_size": 22
        },
        "button_font": {
            "family": "Times",
            "size": 14,
            "weight": "normal",
            "scale_with_window": True,
            "min_size": 10,
            "max_size": 18
        },
        "bg_color": "#FFF8DC",
        "title_fg_color": "#000000",
        "message_fg_color": "#333333",
        "button_bg_color": "#F0FFFF",
        "button_fg_color": "#000000",
        "button_width": 10,
        "button_padx": 10,
        "enable_animation": False,
        "animation_steps": 10,
        "animation_delay": 30,
        "close_on_escape": True,
        "modal": True
    })
    
    # ==================== НАСТРОЙКИ ПОДСКАЗОК ====================
    TOOLTIP_CONFIG: Dict[str, Any] = field(default_factory=lambda: {
        "bg_color": "#FFF8DC",
        "fg_color": "#333333",
        "font": {
            "family": "Times",
            "size": 14,
            "weight": "normal"
        },
        "border_color": "#D4A574",
        "border_width": 2,
        "padding_x": 10,
        "padding_y": 8,
        "offset_x": 20,
        "offset_y": 0,
        "delay": 500
    })
    
    # ==================== НАСТРОЙКИ ДНЕВНИКА ====================
    DIARY_CONFIG: Dict[str, Any] = field(default_factory=lambda: {
        "default_period": 30,
        "max_notes_length": 500,
        "notes_display_length": 120,
        "min_duration": 1,
        "max_duration": 60,
        "default_duration": 10,
        "mood_range": (1, 5),
        "energy_range": (1, 5),
        "default_mood": 3,
        "default_energy": 3,
        "streak_calculation_days": 365
    })
    
    # ==================== ШРИФТЫ ДНЕВНИКА ====================
    DIARY_STATS_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 18, "weight": "bold",
        "scale_with_window": True, "min_size": 14, "max_size": 22
    })
    
    DIARY_ENTRIES_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 18, "weight": "normal",
        "scale_with_window": True, "min_size": 14, "max_size": 22
    })
    
    DIARY_PERIOD_BUTTON_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 13, "weight": "normal",
        "scale_with_window": True, "min_size": 10, "max_size": 16
    })
    
    DIARY_NAV_BUTTON_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 18, "weight": "bold",
        "scale_with_window": True, "min_size": 14, "max_size": 22
    })
    
    DIARY_COUNTER_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 16, "weight": "normal",
        "scale_with_window": True, "min_size": 12, "max_size": 20
    })
    
    DIARY_DATE_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 20, "weight": "bold",
        "scale_with_window": True, "min_size": 16, "max_size": 24
    })
    
    DIARY_COL_HEADER_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 16, "weight": "bold",
        "scale_with_window": True, "min_size": 12, "max_size": 20
    })
    
    DIARY_COMBO_FONT: tuple = ("Times", 14)
    DIARY_SPINBOX_FONT: tuple = ("Times", 16)
    DIARY_NOTES_FONT: tuple = ("Times", 14)
    
    DIARY_STATS_PAGE_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times", "size": 16, "weight": "normal",
        "scale_with_window": True, "min_size": 12, "max_size": 20
    })
    
    # ==================== СТИЛИ ДЛЯ КНОПОК ПЕРЕКЛЮЧЕНИЯ ЯЗЫКА ====================
    LANGUAGE_BUTTON_FONT: Dict[str, Any] = field(default_factory=lambda: {
        "family": "Times",
        "size": 16,
        "weight": "normal",
        "scale_with_window": True,
        "min_size": 12,
        "max_size": 20
    })
    LANGUAGE_BUTTON_WIDTH: float = 0.08
    LANGUAGE_BUTTON_HEIGHT: float = 0.04
    LANGUAGE_BUTTON_Y_RATIO: float = 0.92
    LANGUAGE_BUTTON_GAP: float = 0.02


# Глобальный экземпляр стилей для доступа из любого места
styles = TkinterStyles()
