"""Логика опросника - подбор практики по ответам"""

from typing import Dict, Any, Optional


class SurveyLogic:
    """
    Логика работы опросника.
    Отвечает за хранение ответов и определение результата.
    """
    
    def __init__(self, texts_module):
        """
        Инициализация логики опросника
        
        Args:
            texts_module: Модуль с текстами (texts или texts_en)
        """
        self.texts_module = texts_module
        self.answers: Dict[str, str] = {}
    
    def get_question(self, index: int) -> Dict:
        """
        Получение вопроса по индексу
        
        Args:
            index: Индекс вопроса (0-based)
            
        Returns:
            Словарь с данными вопроса
        """
        if 0 <= index < len(self.texts_module.SURVEY_QUESTIONS):
            return self.texts_module.SURVEY_QUESTIONS[index]
        return self.texts_module.SURVEY_QUESTIONS[0]
    
    def get_questions_count(self) -> int:
        """Количество вопросов в опроснике"""
        return len(self.texts_module.SURVEY_QUESTIONS)
    
    def save_answer(self, question_id: str, value: str):
        """
        Сохранение ответа на вопрос
        
        Args:
            question_id: ID вопроса (например, "purpose")
            value: Значение ответа (например, "calm")
        """
        self.answers[question_id] = value
    
    def get_answer(self, question_id: str) -> Optional[str]:
        """Получение сохраненного ответа"""
        return self.answers.get(question_id)
    
    def get_result(self) -> Dict:
        """
        Получение результата опросника
        
        Returns:
            Словарь с результатом (title, description, tips, practice, page)
        """
        result_key = self.texts_module.get_survey_result(self.answers)
        return self.texts_module.SURVEY_RESULTS.get(result_key, self.texts_module.SURVEY_RESULTS["default"])
    
    def get_recommended_page(self) -> str:
        """Получение имени рекомендуемой страницы для перехода"""
        result = self.get_result()
        return result.get("page", "Prana1BeginnerPage")
    
    def get_recommended_practice_name(self) -> str:
        """Получение названия рекомендуемой практики"""
        result = self.get_result()
        return result.get("practice", "Сама Вритти")
    
    def reset(self):
        """Сброс всех ответов"""
        self.answers = {}
    
    def is_complete(self) -> bool:
        """Проверка, отвечены ли все вопросы"""
        expected_ids = [q["id"] for q in self.texts_module.SURVEY_QUESTIONS]
        return all(q_id in self.answers for q_id in expected_ids)
    
    def get_progress(self) -> tuple:
        """
        Получение прогресса прохождения опросника
        
        Returns:
            (отвеченные_вопросы, всего_вопросов)
        """
        answered = sum(1 for q in self.texts_module.SURVEY_QUESTIONS 
                      if q["id"] in self.answers)
        return answered, len(self.texts_module.SURVEY_QUESTIONS)
