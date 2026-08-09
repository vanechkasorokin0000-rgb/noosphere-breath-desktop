"""
Менеджер дневника - управление записями и статистикой
"""

import json
import os
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
from collections import defaultdict
from .models import DiaryEntry, Statistics


class DiaryManager:
    """
    Управление дневником наблюдений.
    Отвечает за сохранение, загрузку и анализ записей.
    """
    
    def __init__(self, data_dir: str = "diary_data"):
        """
        Инициализация менеджера дневника
        
        Args:
            data_dir: Директория для хранения данных
        """
        self.data_dir = data_dir
        self.diary_file = os.path.join(data_dir, "diary.json")
        self.texts_module = None
        self._ensure_data_dir()
        self.data = self._load_diary()
    
    def _ensure_data_dir(self):
        """Создание директории для данных, если не существует"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_diary(self) -> Dict:
        """Загрузка дневника из файла"""
        if os.path.exists(self.diary_file):
            try:
                with open(self.diary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "entries" not in data:
                        data["entries"] = []
                    return data
            except Exception as e:
                print(f"Ошибка загрузки дневника: {e}")
                return {"entries": []}
        return {"entries": []}
    
    def _save_diary(self) -> bool:
        """Сохранение дневника в файл"""
        try:
            with open(self.diary_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения дневника: {e}")
            return False
    
    def set_texts_module(self, texts_module):
        """Установка модуля с текстами для склонений"""
        self.texts_module = texts_module
    
    def add_entry(self, entry_data: Dict) -> str:
        """
        Добавление или обновление записи
        
        Args:
            entry_data: Данные записи
            
        Returns:
            "added" - новая запись, "updated" - обновлена существующая
        """
        if "date" not in entry_data:
            entry_data["date"] = date.today().strftime("%Y-%m-%d")
        
        if "practices" not in entry_data:
            entry_data["practices"] = []
        
        existing_entry = self.get_entry_by_date(entry_data["date"])
        
        if existing_entry:
            # Обновляем ВСЕ поля (включая списки настроения и энергии)
            existing_entry["practices"] = entry_data["practices"]
            existing_entry["mood_before"] = entry_data.get("mood_before", existing_entry.get("mood_before", 3))
            existing_entry["mood_after"] = entry_data.get("mood_after", existing_entry.get("mood_after", 4))
            existing_entry["energy_before"] = entry_data.get("energy_before", existing_entry.get("energy_before", 3))
            existing_entry["energy_after"] = entry_data.get("energy_after", existing_entry.get("energy_after", 4))
            existing_entry["mood_before_list"] = entry_data.get("mood_before_list", [])
            existing_entry["mood_after_list"] = entry_data.get("mood_after_list", [])
            existing_entry["energy_before_list"] = entry_data.get("energy_before_list", [])
            existing_entry["energy_after_list"] = entry_data.get("energy_after_list", [])
            existing_entry["notes"] = entry_data.get("notes", existing_entry.get("notes", ""))
            
            self._save_diary()
            return "updated"
        else:
            self.data["entries"].append(entry_data)
            self._save_diary()
            return "added"
    
    def get_entry_by_date(self, date_str: str) -> Optional[Dict]:
        """Получение записи по дате"""
        for entry in self.data["entries"]:
            if entry["date"] == date_str:
                return entry
        return None
    
    def get_all_entries(self) -> List[Dict]:
        """Получение всех записей, отсортированных по дате (новые сверху)"""
        return sorted(self.data["entries"], key=lambda x: x["date"], reverse=True)
    
    def get_entries_for_period(self, days: int = 30) -> List[Dict]:
        """Получение записей за определенный период"""
        today = date.today()
        start_date = today - timedelta(days=days)
        
        entries = []
        for entry in self.data["entries"]:
            try:
                entry_date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                if start_date <= entry_date <= today:
                    entries.append(entry)
            except:
                continue
        
        entries.sort(key=lambda x: x["date"], reverse=True)
        return entries
    
    def delete_entry(self, date_str: str):
        """Удаление записи по дате"""
        self.data["entries"] = [e for e in self.data["entries"] if e["date"] != date_str]
        self._save_diary()
    
    def get_statistics(self, days: int = 30) -> Optional[Statistics]:
        """Получение расширенной статистики за период"""
        entries = self.get_entries_for_period(days)
        
        if not entries:
            return None
        
        stats = Statistics(
            total_days=len(entries),
            total_sessions=0,
            total_minutes=0,
            techniques_used=defaultdict(lambda: {"count": 0, "total_minutes": 0}),
            average_mood_before=0.0,
            average_mood_after=0.0,
            average_mood_improvement=0.0,
            average_energy_before=0.0,
            average_energy_after=0.0,
            average_energy_improvement=0.0,
            current_streak=0,
            best_streak=0,
            most_practiced_technique={"name": "", "count": 0}
        )
        
        mood_before_sum = 0
        mood_after_sum = 0
        energy_before_sum = 0
        energy_after_sum = 0
        mood_count = 0
        energy_count = 0
        
        for entry in entries:
            # Сбор информации о практиках
            for practice in entry.get("practices", []):
                stats.total_sessions += 1
                duration = practice.get("duration", 0)
                stats.total_minutes += duration
                
                technique = practice.get("technique", "Неизвестно")
                stats.techniques_used[technique]["count"] += 1
                stats.techniques_used[technique]["total_minutes"] += duration
            
            # Сбор информации о настроении и энергии
            if "mood_before_list" in entry and "mood_after_list" in entry:
                # Используем средние значения из списков за день
                if entry["mood_before_list"] and entry["mood_after_list"]:
                    avg_before = sum(entry["mood_before_list"]) / len(entry["mood_before_list"])
                    avg_after = sum(entry["mood_after_list"]) / len(entry["mood_after_list"])
                    mood_before_sum += avg_before
                    mood_after_sum += avg_after
                    mood_count += 1
            elif "mood_before" in entry and "mood_after" in entry:
                mood_before_sum += entry["mood_before"]
                mood_after_sum += entry["mood_after"]
                mood_count += 1
            
            if "energy_before_list" in entry and "energy_after_list" in entry:
                if entry["energy_before_list"] and entry["energy_after_list"]:
                    avg_before = sum(entry["energy_before_list"]) / len(entry["energy_before_list"])
                    avg_after = sum(entry["energy_after_list"]) / len(entry["energy_after_list"])
                    energy_before_sum += avg_before
                    energy_after_sum += avg_after
                    energy_count += 1
            elif "energy_before" in entry and "energy_after" in entry:
                energy_before_sum += entry["energy_before"]
                energy_after_sum += entry["energy_after"]
                energy_count += 1
        
        if mood_count > 0:
            stats.average_mood_before = mood_before_sum / mood_count
            stats.average_mood_after = mood_after_sum / mood_count
            stats.average_mood_improvement = stats.average_mood_after - stats.average_mood_before
        
        if energy_count > 0:
            stats.average_energy_before = energy_before_sum / energy_count
            stats.average_energy_after = energy_after_sum / energy_count
            stats.average_energy_improvement = stats.average_energy_after - stats.average_energy_before
        
        if stats.techniques_used:
            most_popular = max(stats.techniques_used.items(), key=lambda x: x[1]["count"])
            stats.most_practiced_technique = {
                "name": most_popular[0],
                "count": most_popular[1]["count"]
            }
        
        stats.current_streak, stats.best_streak = self._calculate_streaks()
        
        return stats
    
    def _calculate_streaks(self) -> tuple:
        """Расчет текущей и лучшей серии дней практики (оптимизированная версия O(n))"""
        today = date.today()
        
        # Строим множество дат с записями за O(n)
        dates_with_entries = set()
        for entry in self.data["entries"]:
            dates_with_entries.add(entry["date"])
        
        current_streak = 0
        best_streak = 0
        temp_streak = 0
        
        for i in range(365):
            check_date = today - timedelta(days=i)
            date_str = check_date.strftime("%Y-%m-%d")
            
            if date_str in dates_with_entries:
                temp_streak += 1
                if i == 0:
                    current_streak = temp_streak
            else:
                if temp_streak > best_streak:
                    best_streak = temp_streak
                temp_streak = 0
                if i == 0:
                    continue
        
        if temp_streak > best_streak:
            best_streak = temp_streak
        
        return current_streak, best_streak
    
    def _pluralize(self, number: int, forms: dict) -> str:
        """Правильное склонение числительных"""
        n = abs(number) % 100
        if 11 <= n <= 19:
            return forms["many"]
        n = n % 10
        if n == 1:
            return forms["one"]
        elif 2 <= n <= 4:
            return forms["few"]
        else:
            return forms["many"]
    
    def get_day_word(self, number: int) -> str:
        """Склонение слова 'день' с учетом текущего языка"""
        if self.texts_module and hasattr(self.texts_module, 'DAY_FORMS'):
            forms = self.texts_module.DAY_FORMS
        else:
            forms = {"one": "день", "few": "дня", "many": "дней"}
        return self._pluralize(number, forms)
    
    def get_session_word(self, number: int) -> str:
        """Склонение слова 'сессия' с учетом текущего языка"""
        if self.texts_module and hasattr(self.texts_module, 'SESSION_FORMS'):
            forms = self.texts_module.SESSION_FORMS
        else:
            forms = {"one": "сессия", "few": "сессии", "many": "сессий"}
        return self._pluralize(number, forms)
