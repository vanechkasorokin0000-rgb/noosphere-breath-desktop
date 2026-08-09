"""Главный контроллер приложения - связь между ядром и UI"""

from typing import Any, Optional, Dict, List, Callable
from .models import Language, Statistics
from .diary_manager import DiaryManager
from .survey_logic import SurveyLogic
from .timer_logic import TimerLogic
from .language_manager import LanguageManager


class AppController:
    """
    Главный контроллер приложения.
    Координирует работу всех модулей ядра.
    UI взаимодействует только с этим классом.
    """
    
    def __init__(self):
        """Инициализация контроллера"""
        self.language_manager = LanguageManager()
        self.diary_manager = DiaryManager()
        self.survey_logic: Optional[SurveyLogic] = None
        self.timer_logic: Optional[TimerLogic] = None
        self._page_callbacks: Dict[str, List[Callable]] = {}
        self._app_instance = None  # Ссылка на экземпляр приложения (TkinterApp)
    
    def initialize(self, texts_module_ru: Any, texts_module_en: Any):
        """
        Инициализация контроллера с языковыми модулями
        
        Args:
            texts_module_ru: Модуль с русскими текстами
            texts_module_en: Модуль с английскими текстами
        """
        # Регистрация языков
        self.language_manager.register_module(Language.RUSSIAN, texts_module_ru)
        self.language_manager.register_module(Language.ENGLISH, texts_module_en)
        
        # Регистрация менеджера дневника для обновления текстов
        self.language_manager.register_diary_manager(self.diary_manager)
        
        # Установка начального языка
        self.language_manager.switch_language(Language.RUSSIAN)
        
        # Инициализация зависимых модулей
        self._update_dependencies()
        
        # Подписка на смену языка
        self.language_manager.add_callback(self._on_language_changed)
    
    def set_app_instance(self, app_instance):
        """Установка экземпляра приложения (для прямого доступа к show_frame)"""
        self._app_instance = app_instance
    
    def _update_dependencies(self):
        """Обновление зависимостей при смене языка"""
        current_texts = self.language_manager.get_current_module()
        self.survey_logic = SurveyLogic(current_texts)
        self.timer_logic = TimerLogic(current_texts)
    
    def _on_language_changed(self, texts_module: Any):
        """Обработка смены языка"""
        self._update_dependencies()
        
        # Уведомление UI о смене языка
        self._trigger_callback("language_changed", texts_module)
    
    def register_callback(self, event: str, callback: Callable):
        """
        Регистрация callback для событий
        
        Args:
            event: Название события ("language_changed", "diary_updated", "cleanup", "show_screen")
            callback: Функция для вызова
        """
        if event not in self._page_callbacks:
            self._page_callbacks[event] = []
        self._page_callbacks[event].append(callback)
    
    def _trigger_callback(self, event: str, *args, **kwargs):
        """Вызов всех callback для события"""
        if event in self._page_callbacks:
            for callback in self._page_callbacks[event]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Ошибка в callback {event}: {e}")
    
    def cleanup(self):
        """Очистка ресурсов - вызывает cleanup из UI"""
        self._trigger_callback("cleanup")
    
    def show_frame(self, page_name: str):
        """
        Показ страницы (для Tkinter версии)
        Прямой вызов метода приложения
        """
        if self._app_instance and hasattr(self._app_instance, 'show_frame'):
            self._app_instance.show_frame(page_name)
        else:
            # Fallback на callback систему
            self._trigger_callback("show_frame", page_name)
    
    def show_screen(self, screen_name: str):
        """Показ экрана (для Kivy версии) - перенаправляет в UI"""
        self._trigger_callback("show_screen", screen_name)
    
    # ==================== УПРАВЛЕНИЕ ЯЗЫКОМ ====================
    
    def switch_language(self, lang: str):
        """Переключение языка ("ru" или "en")"""
        self.language_manager.switch_language_from_string(lang)
    
    def get_current_language(self) -> str:
        """Получение текущего языка"""
        return self.language_manager.get_current_language().value
    
    def get_texts(self) -> Any:
        """Получение текущего языкового модуля"""
        return self.language_manager.get_current_module()
    
    # ==================== РАБОТА С ДНЕВНИКОМ ====================
    
    def add_diary_entry(self, entry: Dict) -> str:
        """Добавление записи в дневник"""
        result = self.diary_manager.add_entry(entry)
        self._trigger_callback("diary_updated")
        return result
    
    def get_diary_entries(self, days: int = 30) -> List[Dict]:
        """Получение записей дневника за период"""
        return self.diary_manager.get_entries_for_period(days)
    
    def get_all_diary_entries(self) -> List[Dict]:
        """Получение всех записей дневника"""
        return self.diary_manager.get_all_entries()
    
    def get_diary_entry_by_date(self, date_str: str) -> Optional[Dict]:
        """Получение записи по дате"""
        return self.diary_manager.get_entry_by_date(date_str)
    
    def delete_diary_entry(self, date_str: str):
        """Удаление записи из дневника"""
        self.diary_manager.delete_entry(date_str)
        self._trigger_callback("diary_updated")
    
    def get_diary_statistics(self, days: int = 30) -> Optional[Statistics]:
        """Получение статистики дневника"""
        return self.diary_manager.get_statistics(days)
    
    def get_day_word(self, number: int) -> str:
        """Склонение слова 'день'"""
        return self.diary_manager.get_day_word(number)
    
    def get_session_word(self, number: int) -> str:
        """Склонение слова 'сессия'"""
        return self.diary_manager.get_session_word(number)
    
    # ==================== РАБОТА С ОПРОСНИКОМ ====================
    
    def get_survey_question(self, index: int) -> Dict:
        """Получение вопроса опросника"""
        return self.survey_logic.get_question(index)
    
    def get_survey_questions_count(self) -> int:
        """Количество вопросов в опроснике"""
        return self.survey_logic.get_questions_count()
    
    def save_survey_answer(self, question_id: str, value: str):
        """Сохранение ответа на вопрос"""
        self.survey_logic.save_answer(question_id, value)
    
    def get_survey_answer(self, question_id: str) -> Optional[str]:
        """Получение сохраненного ответа"""
        return self.survey_logic.get_answer(question_id)
    
    def get_survey_result(self) -> Dict:
        """Получение результата опросника"""
        return self.survey_logic.get_result()
    
    def get_recommended_page(self) -> str:
        """Получение рекомендуемой страницы для перехода"""
        return self.survey_logic.get_recommended_page()
    
    def get_recommended_practice(self) -> str:
        """Получение названия рекомендуемой практики"""
        return self.survey_logic.get_recommended_practice_name()
    
    def is_survey_complete(self) -> bool:
        """Проверка, завершен ли опросник"""
        return self.survey_logic.is_complete()
    
    def get_survey_progress(self) -> tuple:
        """Получение прогресса опросника"""
        return self.survey_logic.get_progress()
    
    def reset_survey(self):
        """Сброс опросника"""
        self.survey_logic.reset()
    
    # ==================== РАБОТА С ТАЙМЕРОМ ====================
    
    def start_timer(self, cycles: Dict, total_rounds: int = 3, level: str = "advanced"):
        """Запуск таймера дыхательной практики"""
        self.timer_logic.start(cycles, total_rounds, level)
    
    def pause_timer(self):
        """Пауза таймера"""
        self.timer_logic.pause()
    
    def resume_timer(self):
        """Возобновление таймера"""
        self.timer_logic.resume()
    
    def stop_timer(self):
        """Остановка таймера"""
        self.timer_logic.stop()
    
    def is_timer_running(self) -> bool:
        """Проверка, активен ли таймер"""
        return self.timer_logic.is_running()
    
    def set_timer_callbacks(self, on_tick=None, on_complete=None, 
                           on_stage_change=None, on_round_complete=None):
        """Установка callback для таймера"""
        self.timer_logic.set_callbacks(on_tick, on_complete, on_stage_change, on_round_complete)
    
    # ==================== РАБОТА С ПРАКТИКАМИ ====================
    
    def get_timer_cycles_for_technique(self, technique: str, level: str = "advanced") -> Dict:
        """
        Получение циклов таймера для конкретной техники
        """
        texts = self.get_texts()
        
        cycles_map = {
            "wim_hof": {
                "beginner": {
                    1: [(texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["prepare"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["accelerate"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["basic"], 10)],
                    2: [(texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["warmup"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["halfway"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["final_push"], 10)],
                    3: [(texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["almost"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["keep_pace"], 10),
                        (texts.TIMER_MESSAGES_WIM_HOF_BEGINNER["finish_line"], 10)]
                },
                "advanced": {
                    1: [(texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["prepare"], 12),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["accelerate"], 12),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["basic"], 12)],
                    2: [(texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["warmup"], 12),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["halfway"], 12),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["final_push"], 12)],
                    3: [(texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["almost"], 15),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["keep_pace"], 15),
                        (texts.TIMER_MESSAGES_WIM_HOF_ADVANCED["finish_line"], 15)]
                }
            },
            "prana1": {
                "beginner": {
                    i: [(texts.TIMER_MESSAGES_PRANA1["inhale"], 4),
                        (texts.TIMER_MESSAGES_PRANA1["hold"], 4),
                        (texts.TIMER_MESSAGES_PRANA1["exhale"], 4),
                        (texts.TIMER_MESSAGES_PRANA1["hold"], 4)]
                    for i in range(1, 11)
                },
                "advanced": {
                    i: [(texts.TIMER_MESSAGES_PRANA1["inhale"], 6),
                        (texts.TIMER_MESSAGES_PRANA1["hold"], 6),
                        (texts.TIMER_MESSAGES_PRANA1["exhale"], 6),
                        (texts.TIMER_MESSAGES_PRANA1["hold"], 6)]
                    for i in range(1, 11)
                }
            },
            "prana2": {
                "beginner": {
                    i: [(texts.TIMER_MESSAGES_PRANA2["inhale_left"], 4),
                        (texts.TIMER_MESSAGES_PRANA2["exhale_right"], 4),
                        (texts.TIMER_MESSAGES_PRANA2["inhale_right"], 4),
                        (texts.TIMER_MESSAGES_PRANA2["exhale_left"], 4)]
                    for i in range(1, 11)
                },
                "advanced": {
                    i: [(texts.TIMER_MESSAGES_PRANA2["inhale_left"], 6),
                        (texts.TIMER_MESSAGES_PRANA2["exhale_right"], 6),
                        (texts.TIMER_MESSAGES_PRANA2["inhale_right"], 6),
                        (texts.TIMER_MESSAGES_PRANA2["exhale_left"], 6)]
                    for i in range(1, 11)
                }
            },
            "prana3": {
                "beginner": {
                    i: [(texts.TIMER_MESSAGES_PRANA3["inhale"], 4),
                        (texts.TIMER_MESSAGES_PRANA3["exhale_sound"], 8)]
                    for i in range(1, 8)
                },
                "advanced": {
                    i: [(texts.TIMER_MESSAGES_PRANA3["inhale"], 6),
                        (texts.TIMER_MESSAGES_PRANA3["exhale_sound"], 12)]
                    for i in range(1, 8)
                }
            },
            "addiction": {
                "advanced": {
                    1: [(texts.TIMER_MESSAGES_ADDICTION["prepare"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["start"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["focus"], 10)],
                    2: [(texts.TIMER_MESSAGES_ADDICTION["warmup"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["halfway"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["final"], 10)],
                    3: [(texts.TIMER_MESSAGES_ADDICTION["almost"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["keep"], 10),
                        (texts.TIMER_MESSAGES_ADDICTION["finish"], 10)]
                }
            }
        }
        
        tech_cycles = cycles_map.get(technique, {})
        level_cycles = tech_cycles.get(level, tech_cycles.get("advanced", {}))
        
        return level_cycles
