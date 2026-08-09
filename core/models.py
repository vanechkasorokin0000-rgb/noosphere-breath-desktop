"""Модели данных - классы для хранения информации"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Any, Optional
from enum import Enum


class Language(Enum):
    """Поддерживаемые языки"""
    RUSSIAN = "ru"
    ENGLISH = "en"
    
    @classmethod
    def from_string(cls, lang_str: str) -> 'Language':
        """Создание из строки"""
        if lang_str == "ru":
            return cls.RUSSIAN
        elif lang_str == "en":
            return cls.ENGLISH
        return cls.RUSSIAN


class PracticeLevel(Enum):
    """Уровень практики"""
    BEGINNER = "beginner"
    ADVANCED = "advanced"
    
    @classmethod
    def from_string(cls, level_str: str) -> 'PracticeLevel':
        """Создание из строки"""
        if level_str == "beginner":
            return cls.BEGINNER
        elif level_str == "advanced":
            return cls.ADVANCED
        return cls.BEGINNER


class TechniqueType(Enum):
    """Типы техник"""
    WIM_HOF = "wim_hof"
    PRANA1 = "prana1"
    PRANA2 = "prana2"
    PRANA3 = "prana3"
    ADDICTION_BATTLE = "addiction_battle"
    
    @classmethod
    def from_string(cls, tech_str: str) -> Optional['TechniqueType']:
        """Создание из строки"""
        mapping = {
            "wim_hof": cls.WIM_HOF,
            "prana1": cls.PRANA1,
            "prana2": cls.PRANA2,
            "prana3": cls.PRANA3,
            "addiction_battle": cls.ADDICTION_BATTLE
        }
        return mapping.get(tech_str.lower())


@dataclass
class PracticeEntry:
    """Запись о практике"""
    technique: str
    duration: int
    level: PracticeLevel
    date: date = field(default_factory=date.today)
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return {
            "technique": self.technique,
            "duration": self.duration,
            "level": self.level.value,
            "date": self.date.strftime("%Y-%m-%d")
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PracticeEntry':
        """Создание из словаря"""
        return cls(
            technique=data["technique"],
            duration=data["duration"],
            level=PracticeLevel.from_string(data.get("level", "beginner")),
            date=date.fromisoformat(data.get("date", date.today().isoformat()))
        )


@dataclass
class DiaryEntry:
    """Полная запись дневника"""
    date: str
    practices: List[Dict[str, Any]]
    mood_before: int
    mood_after: int
    energy_before: int
    energy_after: int
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return {
            "date": self.date,
            "practices": self.practices,
            "mood_before": self.mood_before,
            "mood_after": self.mood_after,
            "energy_before": self.energy_before,
            "energy_after": self.energy_after,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiaryEntry':
        """Создание из словаря"""
        return cls(
            date=data["date"],
            practices=data.get("practices", []),
            mood_before=data.get("mood_before", 3),
            mood_after=data.get("mood_after", 4),
            energy_before=data.get("energy_before", 3),
            energy_after=data.get("energy_after", 4),
            notes=data.get("notes", "")
        )
    
    def get_mood_change(self) -> int:
        """Изменение настроения"""
        return self.mood_after - self.mood_before
    
    def get_energy_change(self) -> int:
        """Изменение энергии"""
        return self.energy_after - self.energy_before
    
    def get_total_duration(self) -> int:
        """Общая длительность всех практик"""
        return sum(p.get("duration", 0) for p in self.practices)


@dataclass
class Statistics:
    """Статистика практик"""
    total_days: int
    total_sessions: int
    total_minutes: int
    techniques_used: Dict[str, Dict[str, int]]
    average_mood_before: float
    average_mood_after: float
    average_mood_improvement: float
    average_energy_before: float
    average_energy_after: float
    average_energy_improvement: float
    current_streak: int
    best_streak: int
    most_practiced_technique: Dict[str, Any]
    
    def get_formatted_mood(self) -> str:
        """Форматированное изменение настроения"""
        imp = self.average_mood_improvement
        if imp > 0:
            return f"+{imp:.1f}"
        elif imp < 0:
            return f"{imp:.1f}"
        return "0"
    
    def get_formatted_energy(self) -> str:
        """Форматированное изменение энергии"""
        imp = self.average_energy_improvement
        if imp > 0:
            return f"+{imp:.1f}"
        elif imp < 0:
            return f"{imp:.1f}"
        return "0"


@dataclass
class TimerState:
    """Состояние таймера"""
    is_active: bool = False
    is_paused: bool = False
    time_left: int = 0
    current_round: int = 1
    current_cycle: int = 1
    current_stage: str = ""
    current_stage_message: str = ""
    stages: List[tuple] = field(default_factory=list)
    original_stages: List[tuple] = field(default_factory=list)
    is_preview_phase: bool = False
    total_rounds: int = 3
    
    def reset(self):
        """Сброс состояния"""
        self.is_active = False
        self.is_paused = False
        self.time_left = 0
        self.current_round = 1
        self.current_cycle = 1
        self.current_stage = ""
        self.current_stage_message = ""
        self.stages = []
        self.original_stages = []
        self.is_preview_phase = False
