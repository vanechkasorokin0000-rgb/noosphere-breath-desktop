"""Управление языками приложения"""

from typing import Dict, Any, Callable, List, Optional
from .models import Language


class LanguageManager:
    """
    Менеджер языков.
    Отвечает за переключение между языками и уведомление UI.
    """
    
    def __init__(self):
        """Инициализация менеджера языков"""
        self._current_language = Language.RUSSIAN
        self._modules: Dict[Language, Any] = {
            Language.RUSSIAN: None,
            Language.ENGLISH: None
        }
        self._callbacks: List[Callable] = []
        self._diary_managers: List[Any] = []
    
    def register_module(self, language: Language, module: Any):
        """
        Регистрация языкового модуля
        
        Args:
            language: Язык
            module: Модуль с текстами (texts или texts_en)
        """
        self._modules[language] = module
    
    def register_diary_manager(self, diary_manager):
        """Регистрация менеджера дневника для обновления текстов"""
        self._diary_managers.append(diary_manager)
    
    def switch_language(self, language: Language):
        """
        Переключение языка
        
        Args:
            language: Новый язык
        """
        if language in self._modules and self._modules[language]:
            self._current_language = language
            
            # Обновляем тексты в зарегистрированных менеджерах
            current_module = self.get_current_module()
            for diary_manager in self._diary_managers:
                diary_manager.set_texts_module(current_module)
            
            # Уведомляем подписчиков
            self._notify_callbacks()
    
    def switch_language_from_string(self, lang_str: str):
        """Переключение языка из строки ("ru" или "en")"""
        language = Language.from_string(lang_str)
        self.switch_language(language)
    
    def get_current_module(self) -> Any:
        """Получение текущего языкового модуля"""
        return self._modules[self._current_language]
    
    def get_current_language(self) -> Language:
        """Получение текущего языка"""
        return self._current_language
    
    def add_callback(self, callback: Callable[[Any], None]):
        """
        Добавление callback при смене языка
        
        Args:
            callback: Функция, принимающая новый языковой модуль
        """
        self._callbacks.append(callback)
    
    def remove_callback(self, callback: Callable):
        """Удаление callback"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def _notify_callbacks(self):
        """Уведомление всех подписчиков о смене языка"""
        current_module = self.get_current_module()
        for callback in self._callbacks:
            try:
                callback(current_module)
            except Exception as e:
                print(f"Ошибка в callback при смене языка: {e}")
    
    def get_text(self, key: str, *args, **kwargs) -> str:
        """
        Получение текста по ключу (упрощенный доступ)
        
        Args:
            key: Ключ в формате "SECTION.KEY" или просто "KEY"
            
        Returns:
            Текст на текущем языке
        """
        module = self.get_current_module()
        
        # Поддержка вложенных ключей
        parts = key.split('.')
        current = module
        for part in parts:
            if hasattr(current, part):
                current = getattr(current, part)
            else:
                return key
        
        if callable(current):
            return str(current(*args, **kwargs))
        return str(current)
