"""Логика таймера для дыхательных практик"""

import threading
import time
from typing import List, Tuple, Callable, Optional, Dict
from .models import TimerState, PracticeLevel


class TimerLogic:
    """
    Логика работы таймера для дыхательных практик.
    Управляет временем, этапами и уведомлениями.
    """
    
    def __init__(self, texts_module):
        """
        Инициализация логики таймера
        
        Args:
            texts_module: Модуль с текстами для сообщений таймера
        """
        self.texts_module = texts_module
        self.state = TimerState()
        self._timer_thread: Optional[threading.Timer] = None
        self._lock = threading.Lock()
        
        # Callback функции для UI
        self._on_tick = None
        self._on_complete = None
        self._on_stage_change = None
        self._on_round_complete = None
    
    def set_callbacks(self, 
                      on_tick: Callable = None,
                      on_complete: Callable = None,
                      on_stage_change: Callable = None,
                      on_round_complete: Callable = None):
        """
        Установка callback-функций для UI
        
        Args:
            on_tick: Вызывается при каждом тике таймера (time_left, stage)
            on_complete: Вызывается при завершении всей практики
            on_stage_change: Вызывается при смене этапа (stage, is_preview, duration)
            on_round_complete: Вызывается при завершении раунда
        """
        self._on_tick = on_tick
        self._on_complete = on_complete
        self._on_stage_change = on_stage_change
        self._on_round_complete = on_round_complete
    
    def start(self, cycles: Dict[int, List[Tuple[str, int]]], 
              total_rounds: int = 3, 
              level: str = "advanced"):
        """
        Запуск таймера
        
        Args:
            cycles: Словарь с циклами (номер раунда -> список этапов)
            total_rounds: Общее количество раундов
            level: Уровень практики ("beginner" или "advanced")
        """
        with self._lock:
            self._stop_timer()
            self.state.reset()
            
            # Корректировка длительности в зависимости от уровня
            duration_multiplier = self.texts_module.LEVEL_DURATION_MULTIPLIER.get(level, 1.0)
            
            adjusted_cycles = {}
            for round_num, stages in cycles.items():
                adjusted_stages = []
                for message, duration in stages:
                    adjusted_duration = max(1, int(duration * duration_multiplier))
                    adjusted_stages.append((message, adjusted_duration))
                adjusted_cycles[round_num] = adjusted_stages
            
            self.state.total_rounds = total_rounds
            self.state.is_active = True
            self.state.original_stages = adjusted_cycles.get(1, []).copy()
            self.state.stages = self.state.original_stages.copy()
            
            self._start_preview_phase()
    
    def _start_preview_phase(self):
        """Начало фазы предпросмотра (1 секунда перед каждым этапом)"""
        if self.state.stages and self.state.is_active and not self.state.is_paused:
            self.state.is_preview_phase = True
            stage_message, duration = self.state.stages[0]
            self.state.current_stage_message = stage_message
            
            if self._on_stage_change:
                self._on_stage_change(stage_message, True, 1)
            
            self.state.time_left = 1
            self._start_timer(self._start_main_phase)
    
    def _start_main_phase(self):
        """Начало основной фазы этапа"""
        if self.state.stages and self.state.is_active and not self.state.is_paused:
            self.state.is_preview_phase = False
            stage_message, duration = self.state.stages.pop(0)
            self.state.current_stage_message = stage_message
            self.state.time_left = duration
            
            if self._on_stage_change:
                self._on_stage_change(stage_message, False, duration)
            
            self._start_timer(self._start_preview_phase)
        else:
            self._complete_round()
    
    def _start_timer(self, next_phase: Callable):
        """Запуск обратного отсчета"""
        if self._timer_thread:
            self._timer_thread.cancel()
        
        self._timer_thread = threading.Timer(1.0, lambda: self._update_timer(next_phase))
        self._timer_thread.daemon = True
        self._timer_thread.start()
    
    def _update_timer(self, next_phase: Callable):
        """Обновление таймера (вызывается каждую секунду)"""
        with self._lock:
            if not self.state.is_active or self.state.is_paused:
                return
            
            if self.state.time_left > 0:
                if self._on_tick:
                    self._on_tick(self.state.time_left, self.state.current_stage_message)
                
                self.state.time_left -= 1
                self._start_timer(next_phase)
            elif self.state.time_left == 0:
                if next_phase:
                    next_phase()
    
    def _complete_round(self):
        """Завершение текущего раунда"""
        self.state.current_round += 1
        
        if self._on_round_complete:
            self._on_round_complete(self.state.current_round - 1, self.state.total_rounds)
        
        if self.state.current_round <= self.state.total_rounds:
            self.state.current_cycle += 1
            self.state.original_stages = self._get_cycles_for_round().get(
                self.state.current_cycle, 
                self._get_cycles_for_round().get(1, [])
            ).copy()
            self.state.stages = self.state.original_stages.copy()
            self._start_preview_phase()
        else:
            self._complete_practice()
    
    def _complete_practice(self):
        """Завершение всей практики"""
        self.state.is_active = False
        if self._on_complete:
            self._on_complete()
    
    def _get_cycles_for_round(self) -> Dict[int, List[Tuple[str, int]]]:
        """
        Получение циклов для текущего раунда.
        Должно быть переопределено в подклассах или передано из UI.
        """
        # Базовый метод - возвращает пустой словарь
        # В реальном использовании циклы передаются через start()
        return {}
    
    def pause(self):
        """Пауза таймера"""
        with self._lock:
            if self.state.is_active and not self.state.is_paused:
                self.state.is_paused = True
                if self._timer_thread:
                    self._timer_thread.cancel()
    
    def resume(self):
        """Возобновление таймера"""
        with self._lock:
            if self.state.is_active and self.state.is_paused:
                self.state.is_paused = False
                if self.state.is_preview_phase:
                    self._start_timer(self._start_main_phase)
                elif self.state.stages:
                    self._start_timer(self._start_preview_phase)
                else:
                    self._start_timer(self._complete_round)
    
    def stop(self):
        """Остановка таймера"""
        with self._lock:
            self._stop_timer()
            self.state.is_active = False
    
    def _stop_timer(self):
        """Внутренняя остановка таймера"""
        if self._timer_thread:
            self._timer_thread.cancel()
            self._timer_thread = None
    
    def is_running(self) -> bool:
        """Проверка, активен ли таймер"""
        return self.state.is_active and not self.state.is_paused
    
    def get_current_time(self) -> int:
        """Получение оставшегося времени"""
        return self.state.time_left
    
    def get_current_stage(self) -> str:
        """Получение названия текущего этапа"""
        return self.state.current_stage_message
    
    def get_progress(self) -> tuple:
        """Получение прогресса (текущий_раунд, всего_раундов)"""
        return self.state.current_round - 1, self.state.total_rounds
