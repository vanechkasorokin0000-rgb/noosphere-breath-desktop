"""
Страницы дневника наблюдений
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from core.app_controller import AppController

from ui.tkinter.base_page import PageWithBackground
from ui.tkinter.dialogs import CustomDialog


class DiaryStartPage(PageWithBackground):
    """Стартовая страница дневника"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.create_title(self.texts.DIARY_TITLES.get("start", "Дневник наблюдений"), y_ratio=0.03)
        
        self.create_scrollable_label(
            text=self.texts.DIARY_START_DESCRIPTION,
            width_ratio=0.70, height_ratio=0.4, y_ratio=0.13,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.SURVEY_FONTS["description"],
            justify="center"  # Добавлено
        )
        
        stats = self.controller.get_diary_statistics(30)
        
        if stats and stats.total_days > 0:
            days_word = self.controller.get_day_word(stats.total_days)
            sessions_word = self.controller.get_session_word(stats.total_sessions)
            
            quick_stats = f" {self.texts.DIARY_QUICK_STATS_PREFIX} {stats.total_days} {days_word} {self.texts.DIARY_PRACTICE_TEXT}, {stats.total_sessions} {sessions_word}, {stats.total_minutes} {self.texts.DIARY_MINUTES_TEXT}"
            
            self.create_rounded_label(
                text=quick_stats,
                width_ratio=0.4, height_ratio=0.08, y_ratio=0.55,
                bg_color=self.styles.SURVEY_COLORS["label_bg"],
                font_config=self.styles.DIARY_STATS_FONT,
                border_radius=self.styles.SURVEY_BORDER_RADIUS
            )
            button_y = 0.67
        else:
            self.create_rounded_label(
                text=self.texts.DIARY_START_MESSAGE,
                width_ratio=0.5, height_ratio=0.06, y_ratio=0.55,
                bg_color=self.styles.SURVEY_COLORS["label_bg"],
                font_config=self.styles.SURVEY_FONTS["description"],
                border_radius=self.styles.SURVEY_BORDER_RADIUS
            )
            button_y = 0.65
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("open", "Открыть дневник"),
            command=lambda: controller.show_frame("DiaryViewPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=button_y,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("add_entry", "Добавить запись"),
            command=lambda: controller.show_frame("DiaryAddPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=button_y + 0.08,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("statistics", "Статистика"),
            command=lambda: controller.show_frame("DiaryStatisticsPage"),
            width_ratio=0.25, height_ratio=0.06, y_ratio=button_y + 0.16,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: controller.show_frame("StartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=button_y + 0.24
        )

class DiaryViewPage(PageWithBackground):
    """Страница просмотра записей дневника"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.current_period = self.styles.DIARY_CONFIG.get("default_period", 30)
        self.current_entry_index = 0
        self.entries = []
        self._update_in_progress = False
        
        self.create_title(self.texts.DIARY_TITLES.get("view", "Мои записи"), y_ratio=0.03)
        
        self._create_period_buttons()
        self._create_stats_label()
        self._create_entries_text_widget()
        self._create_navigation_buttons()
        self._create_action_buttons()
        
        self.after(100, self.update_view)
    
    def _create_period_buttons(self):
        """Создание кнопок выбора периода"""
        periods = [
            (self.texts.DIARY_PERIODS.get("7_days", "7 дней"), 7),
            (self.texts.DIARY_PERIODS.get("30_days", "30 дней"), 30),
            (self.texts.DIARY_PERIODS.get("90_days", "90 дней"), 90),
            (self.texts.DIARY_PERIODS.get("year", "Год"), 365)
        ]
        
        button_width = 0.08
        gap = 0.02
        total_width = len(periods) * button_width + (len(periods) - 1) * gap
        start_x = (1 - total_width) / 2
        
        for i, (text, days) in enumerate(periods):
            self.create_button(
                text=text,
                command=lambda d=days: self._change_period(d),
                width_ratio=button_width, height_ratio=0.03, y_ratio=0.11,
                x_ratio=start_x + i * (button_width + gap),
                font_config=self.styles.DIARY_PERIOD_BUTTON_FONT
            )
    
    def _create_stats_label(self):
        """Создание метки со статистикой"""
        self.stats_label = self.create_rounded_label(
            text="", width_ratio=0.5, height_ratio=0.05, y_ratio=0.17,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.DIARY_STATS_FONT,
            border_radius=self.styles.SURVEY_BORDER_RADIUS
        )
    
    def _create_entries_text_widget(self):
        """Создание текстового виджета с прокруткой для отображения записей"""
        # Создаем фрейм-контейнер
        text_frame = tk.Frame(self.canvas, bg=self.styles.COLORS["label_bg"])
        text_frame.place(relx=0.15, rely=0.24, relwidth=0.7, relheight=0.35)
        
        # Создаем Text виджет
        self.entries_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Times", 14),
            bg=self.styles.COLORS["label_bg"],
            fg="#000000",
            padx=20,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5,
            relief="sunken",
            borderwidth=1,
            highlightthickness=0
        )
        
        # Добавляем Scrollbar
        scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.entries_text.yview,
            bg="#D4A574",
            troughcolor="#FFF8DC",
            activebackground="#C4A474"
        )
        self.entries_text.configure(yscrollcommand=scrollbar.set)
        
        # Размещаем виджеты
        scrollbar.pack(side="right", fill="y")
        self.entries_text.pack(side="left", fill="both", expand=True)
        
        # Настройка тегов форматирования
        self.entries_text.tag_configure("center", justify="center", font=("Times", 16, "bold"), foreground="#8B4513")
        self.entries_text.tag_configure("title", font=("Times", 14, "bold"), foreground="#A0522D")
        self.entries_text.tag_configure("subtitle", font=("Times", 14, "bold"), foreground="#A0522D")
        self.entries_text.tag_configure("normal", font=("Times", 14), foreground="#000000")
        self.entries_text.tag_configure("mood", font=("Times", 14), foreground="#2E8B57")
        self.entries_text.tag_configure("energy", font=("Times", 14), foreground="#4169E1")
        
        # Делаем виджет только для чтения
        self.entries_text.configure(state="disabled")
    
    def _create_navigation_buttons(self):
        """Создание кнопок навигации между записями"""
        nav_total_width = 0.22
        nav_start_x = (1 - nav_total_width) / 2
        
        self.prev_button = self.create_button(
            text="←", command=lambda: self._change_entry(-1),
            width_ratio=0.06, height_ratio=0.04, y_ratio=0.61, x_ratio=nav_start_x,
            font_config=self.styles.DIARY_NAV_BUTTON_FONT
        )
        
        self.entry_counter_label = self.create_label(
            text="", width_ratio=0.08, height_ratio=0.04, y_ratio=0.61,
            x_ratio=nav_start_x + 0.07,
            font_config=self.styles.DIARY_COUNTER_FONT
        )
        
        self.next_button = self.create_button(
            text="→", command=lambda: self._change_entry(1),
            width_ratio=0.06, height_ratio=0.04, y_ratio=0.61, x_ratio=nav_start_x + 0.16,
            font_config=self.styles.DIARY_NAV_BUTTON_FONT
        )
    
    def _create_action_buttons(self):
        """Создание кнопок действий"""
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("add_entry", "Добавить запись"),
            command=lambda: self.controller.show_frame("DiaryAddPage"),
            width_ratio=0.18, height_ratio=0.05, y_ratio=0.68,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("statistics", "Статистика"),
            command=lambda: self.controller.show_frame("DiaryStatisticsPage"),
            width_ratio=0.18, height_ratio=0.05, y_ratio=0.74,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("delete", "Удалить запись"),
            command=self._show_delete_confirmation,
            width_ratio=0.18, height_ratio=0.05, y_ratio=0.80,
            bg_color="#FFB2B2", text_color="#8B0000",
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: self.controller.show_frame("DiaryStartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.86
        )
    
    def _change_period(self, days: int):
        self.current_period = days
        self.current_entry_index = 0
        self.update_view()
    
    def _change_entry(self, delta: int):
        if self.entries:
            self.current_entry_index = (self.current_entry_index + delta) % len(self.entries)
            self.update_view()
    
    def _show_delete_confirmation(self):
        if not self.entries or self.current_entry_index >= len(self.entries):
            return
        
        entry = self.entries[self.current_entry_index]
        date_str = entry["date"]
        
        dialog = CustomDialog(
            parent=self, title=self.texts.DIALOG_MESSAGES.get("delete_title", "Подтверждение удаления"),
            message=f"{self.texts.DIALOG_MESSAGES.get('delete_confirmation', 'Вы действительно хотите удалить запись за')} {date_str}?\n\n{self.texts.DIALOG_MESSAGES.get('delete_warning', 'Это действие нельзя отменить.')}",
            button_texts=[
                self.texts.DIALOG_MESSAGES.get("delete_yes", "Да, удалить"),
                self.texts.DIALOG_MESSAGES.get("delete_no", "Отмена")
            ],
            default_button=1, bg_image=self.original_bg_image
        )
        
        result = dialog.show()
        if result == self.texts.DIALOG_MESSAGES.get("delete_yes", "Да, удалить"):
            self.controller.delete_diary_entry(date_str)
            self.update_view()
    
    def update_view(self):
        """Обновление отображения"""
        if self._update_in_progress:
            return
        self._update_in_progress = True
        
        try:
            dm = self.controller
            stats = dm.get_diary_statistics(self.current_period)
            self.entries = dm.get_diary_entries(self.current_period)
            
            if stats and stats.total_days > 0:
                days_word = dm.get_day_word(stats.total_days)
                sessions_word = dm.get_session_word(stats.total_sessions)
                stats_text = f"{stats.total_days} {days_word}, {stats.total_sessions} {sessions_word}, {stats.total_minutes} {self.texts.DIARY_MINUTES_TEXT}"
                if stats.current_streak > 1:
                    streak_word = dm.get_day_word(stats.current_streak)
                    stats_text += f" | 🔥 {stats.current_streak} {streak_word}"
            else:
                stats_text = self.texts.DIARY_NO_ENTRIES_TEXT
            
            self.stats_label.config(text=stats_text)
            self._update_entries_content()
            
        finally:
            self._update_in_progress = False
    
    def _update_entries_content(self):
        """Обновление содержимого текстового виджета"""
        # Разблокируем виджет для редактирования
        self.entries_text.configure(state="normal")
        self.entries_text.delete("1.0", tk.END)
        
        if self.entries and self.current_entry_index < len(self.entries):
            entry = self.entries[self.current_entry_index]
            text_content = self._build_entry_text(entry)
            
            # Вставляем текст
            self.entries_text.insert("1.0", text_content)
            
            # Применяем центрирование ко всему тексту через тег
            self.entries_text.tag_add("center", "1.0", "end")
            
            # Применяем теги форматирования поверх центрирования
            self._apply_text_tags()
            
            self.entry_counter_label.config(text=f"{self.current_entry_index + 1}/{len(self.entries)}")
            
            if len(self.entries) <= 1:
                self.prev_button.config(state="disabled")
                self.next_button.config(state="disabled")
            else:
                self.prev_button.config(state="normal")
                self.next_button.config(state="normal")
        else:
            no_entry_text = f"\n\n{'='*55}\n\nНЕТ ЗАПИСЕЙ\n\n{'='*55}\n"
            self.entries_text.insert("1.0", no_entry_text)
            self.entries_text.tag_add("center", "1.0", "end")
            
            self.entry_counter_label.config(text="0/0")
            self.prev_button.config(state="disabled")
            self.next_button.config(state="disabled")
        
        # Блокируем виджет обратно
        self.entries_text.configure(state="disabled")
    
    
    def _build_entry_text(self, entry: dict) -> str:
        """Формирование текста для отображения записи с поддержкой многоязычности"""
        lines = []
        
        # Заголовок с датой
        lines.append("=" * 55 + "\n")
        lines.append(f"📅 {entry['date']}\n")
        lines.append("=" * 55 + "\n\n")
        
        practices = entry.get("practices", [])
        if practices:
            lines.append(f"{self.texts.DIARY_TECHNIQUE_SECTION.upper()}\n")
            lines.append("-" * 45 + "\n\n")
            
            grouped_practices = defaultdict(list)
            for practice in practices:
                technique = practice.get("technique", "Неизвестно")
                level = practice.get("level", "")
                key = f"{technique}|{level}"
                grouped_practices[key].append(practice)
            
            for key, group_practices in grouped_practices.items():
                technique = group_practices[0].get("technique", "Неизвестно")
                level = group_practices[0].get("level", "")
                level_text = f" ({self.texts.DIARY_BEGINNER_TEXT if level == 'beginner' else self.texts.DIARY_ADVANCED_TEXT})" if level else ""
                
                lines.append(f"  • {technique}{level_text}\n")
                
                for practice in group_practices:
                    duration = practice.get("duration", 0)
                    session_word = self.texts.DIARY_ONE_SESSION if duration == 1 else self.texts.DIARY_SESSION
                    lines.append(f"      → 1 {session_word}, {duration} {self.texts.DIARY_MINUTES_ABBR}\n")
                lines.append("\n")
        
        # Настроение
        mood_changes = []
        if "mood_before_list" in entry and "mood_after_list" in entry:
            for before, after in zip(entry["mood_before_list"], entry["mood_after_list"]):
                mood_changes.append(after - before)
        elif "mood_before" in entry and "mood_after" in entry:
            mood_changes.append(entry["mood_after"] - entry["mood_before"])
        
        if mood_changes:
            avg_mood_change = sum(mood_changes) / len(mood_changes)
            lines.append("\n" + "-" * 45 + "\n")
            if avg_mood_change > 0:
                lines.append(f"😊 {self.texts.DIARY_MOOD_LABEL.upper()}: +{avg_mood_change:.1f}\n")
            elif avg_mood_change < 0:
                lines.append(f"😊 {self.texts.DIARY_MOOD_LABEL.upper()}: {avg_mood_change:.1f}\n")
            else:
                lines.append(f"😊 {self.texts.DIARY_MOOD_LABEL.upper()}: {self.texts.DIARY_NO_CHANGE}\n")
        
        # Энергия
        energy_changes = []
        if "energy_before_list" in entry and "energy_after_list" in entry:
            for before, after in zip(entry["energy_before_list"], entry["energy_after_list"]):
                energy_changes.append(after - before)
        elif "energy_before" in entry and "energy_after" in entry:
            energy_changes.append(entry["energy_after"] - entry["energy_before"])
        
        if energy_changes:
            avg_energy_change = sum(energy_changes) / len(energy_changes)
            if avg_energy_change > 0:
                lines.append(f"⚡ {self.texts.DIARY_ENERGY_LABEL.upper()}: +{avg_energy_change:.1f}\n")
            elif avg_energy_change < 0:
                lines.append(f"⚡ {self.texts.DIARY_ENERGY_LABEL.upper()}: {avg_energy_change:.1f}\n")
            else:
                lines.append(f"⚡ {self.texts.DIARY_ENERGY_LABEL.upper()}: {self.texts.DIARY_NO_CHANGE}\n")
        
        lines.append("\n" + "-" * 45 + "\n")
        
        # Заметки
        notes_exist = False
        if practices:
            lines.append(f"{self.texts.DIARY_NOTES_SECTION.upper()}\n\n")
            
            grouped_notes = defaultdict(list)
            for practice in practices:
                technique = practice.get("technique", "Неизвестно")
                level = practice.get("level", "")
                duration = practice.get("duration", 0)
                notes = practice.get("notes", "")
                key = f"{technique}|{level}"
                if notes and notes.strip():
                    notes_exist = True
                    grouped_notes[key].append({
                        "duration": duration,
                        "notes": notes
                    })
            
            if notes_exist:
                for key, notes_list in grouped_notes.items():
                    technique = key.split("|")[0]
                    level = key.split("|")[1] if len(key.split("|")) > 1 else ""
                    level_text = f" ({self.texts.DIARY_BEGINNER_TEXT if level == 'beginner' else self.texts.DIARY_ADVANCED_TEXT})" if level else ""
                    
                    lines.append(f"  • {technique}{level_text}\n")
                    for note_item in notes_list:
                        duration = note_item["duration"]
                        notes_text = note_item["notes"]
                        lines.append(f"      → {duration} {self.texts.DIARY_MINUTES_ABBR}: {notes_text}\n")
                    lines.append("\n")
            else:
                lines.pop()
                lines.append(f"{self.texts.DIARY_NO_NOTES}\n")
        else:
            if "notes" in entry and entry["notes"]:
                lines.append(f"{self.texts.DIARY_NOTES_SECTION.upper()}\n\n{entry['notes']}\n")
            else:
                lines.append(f"{self.texts.DIARY_NOTES_SECTION.upper()}\n\n{self.texts.DIARY_NO_NOTES}\n")
        
        lines.append("\n" + "=" * 55 + "\n")
        
        return "".join(lines)
    
    def _apply_text_tags(self):
        """Применение тегов форматирования к тексту поверх центрирования"""
        content = self.entries_text.get("1.0", tk.END)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Заголовок с датой (строки с "===" и датой)
            if line_stripped.startswith("===") or "📅" in line_stripped:
                self.entries_text.tag_add("title", f"{i}.0", f"{i}.end")
            elif line_stripped.startswith("ТЕХНИКА:"):
                self.entries_text.tag_add("subtitle", f"{i}.0", f"{i}.end")
            elif line_stripped.startswith("ЗАМЕТКИ:"):
                self.entries_text.tag_add("subtitle", f"{i}.0", f"{i}.end")
            elif "НАСТРОЕНИЕ" in line_stripped or line_stripped.startswith("😊"):
                self.entries_text.tag_add("mood", f"{i}.0", f"{i}.end")
            elif "ЭНЕРГИЯ" in line_stripped or line_stripped.startswith("⚡"):
                self.entries_text.tag_add("energy", f"{i}.0", f"{i}.end")
            elif line_stripped.startswith("•"):
                self.entries_text.tag_add("subtitle", f"{i}.0", f"{i}.end")
    
    def update_widget_sizes_and_positions(self):
        """Обновление размеров и позиций виджетов"""
        super().update_widget_sizes_and_positions()
        if hasattr(self, 'entries_text') and self.entries_text.winfo_exists():
            # Обновляем центрирование при изменении размера
            if self.entries and self.current_entry_index < len(self.entries):
                self.entries_text.tag_add("center", "1.0", "end")


class DiaryAddPage(PageWithBackground):
    """Страница добавления/редактирования записи"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image, edit_date: Optional[str] = None):
        super().__init__(parent, controller, bg_image)
        
        self.edit_date = edit_date
        
        if edit_date:
            existing_entry = controller.get_diary_entry_by_date(edit_date)
            self.create_title(f"{self.texts.DIARY_TITLES.get('edit', 'Редактирование записи за')} {edit_date}", y_ratio=0.03)
        else:
            existing_entry = None
            self.create_title(self.texts.DIARY_TITLES.get("add", "Новая запись"), y_ratio=0.03)
        
        entry_date = edit_date if edit_date else date.today().strftime("%Y-%m-%d")
        
        self.create_label(
            text=f"📅 {entry_date}",
            width_ratio=0.3, height_ratio=0.04, y_ratio=0.10,
            font_config=self.styles.DIARY_DATE_FONT
        )
        
        self.create_label(
            text=self.texts.DIARY_SECTION_PRACTICE,
            width_ratio=0.3, height_ratio=0.04, y_ratio=0.15,
            font_config=self.styles.FONTS["label_title"]
        )
        
        self._create_practice_inputs()
        self._create_mood_energy_inputs()
        self._create_notes_input()
        
        if existing_entry:
            self._load_existing_entry(existing_entry)
        
        self._create_save_buttons()
    
    def _create_practice_inputs(self):
        """Создание виджетов для ввода практики"""
        total_cols_width = 0.55
        col_start_x = (1 - total_cols_width) / 2
        
        self.create_label(
            text=self.texts.DIARY_COL_TECHNIQUE,
            width_ratio=0.22, height_ratio=0.04, y_ratio=0.20, x_ratio=col_start_x,
            font_config=self.styles.DIARY_COL_HEADER_FONT
        )
        self.create_label(
            text=self.texts.DIARY_COL_CATEGORY,
            width_ratio=0.15, height_ratio=0.04, y_ratio=0.20, x_ratio=col_start_x + 0.23,
            font_config=self.styles.DIARY_COL_HEADER_FONT
        )
        self.create_label(
            text=self.texts.DIARY_COL_TIME,
            width_ratio=0.12, height_ratio=0.04, y_ratio=0.20, x_ratio=col_start_x + 0.40,
            font_config=self.styles.DIARY_COL_HEADER_FONT
        )
        
        self.technique_var = tk.StringVar(value=self.texts.DIARY_TECHNIQUES[0])
        technique_combo = ttk.Combobox(
            self.canvas, textvariable=self.technique_var,
            values=self.texts.DIARY_TECHNIQUES, state="readonly",
            font=self.styles.DIARY_COMBO_FONT
        )
        technique_combo.place(relx=col_start_x, rely=0.25, relwidth=0.22, relheight=0.05)
        
        self.level_var = tk.StringVar(value=self.texts.DIARY_LEVEL_BEGINNER)
        level_combo = ttk.Combobox(
            self.canvas, textvariable=self.level_var,
            values=[self.texts.DIARY_LEVEL_BEGINNER, self.texts.DIARY_LEVEL_ADVANCED],
            state="readonly", font=self.styles.DIARY_COMBO_FONT
        )
        level_combo.place(relx=col_start_x + 0.23, rely=0.25, relwidth=0.15, relheight=0.05)
        
        self.duration_var = tk.IntVar(value=self.styles.DIARY_CONFIG.get("default_duration", 10))
        duration_spinbox = tk.Spinbox(
            self.canvas, from_=self.styles.DIARY_CONFIG.get("min_duration", 1),
            to=self.styles.DIARY_CONFIG.get("max_duration", 60),
            textvariable=self.duration_var, font=self.styles.DIARY_SPINBOX_FONT,
            justify="center", width=5, state="readonly"
        )
        duration_spinbox.place(relx=col_start_x + 0.40, rely=0.25, relwidth=0.12, relheight=0.05)
    
    def _create_mood_energy_inputs(self):
        """Создание виджетов для ввода настроения и энергии"""
        mood_energy_total_width = 0.7
        start_x = (1 - mood_energy_total_width) / 2
        
        self.create_label(
            text=self.texts.DIARY_MOOD_TITLE,
            width_ratio=0.3, height_ratio=0.04, y_ratio=0.33, x_ratio=start_x,
            font_config=self.styles.FONTS["label_title"]
        )
        self.create_label(
            text=self.texts.DIARY_ENERGY_TITLE,
            width_ratio=0.3, height_ratio=0.04, y_ratio=0.33, x_ratio=start_x + 0.40,
            font_config=self.styles.FONTS["label_title"]
        )
        
        self.create_label(
            text=self.texts.DIARY_BEFORE_TEXT,
            width_ratio=0.05, height_ratio=0.03, y_ratio=0.39, x_ratio=start_x,
            font_config=self.styles.FONTS["label_small"]
        )
        
        self.mood_before_var = tk.IntVar(value=self.styles.DIARY_CONFIG.get("default_mood", 3))
        mood_before_spinbox = tk.Spinbox(
            self.canvas, from_=1, to=5, textvariable=self.mood_before_var,
            font=self.styles.DIARY_SPINBOX_FONT, justify="center", width=3, state="readonly"
        )
        mood_before_spinbox.place(relx=start_x + 0.06, rely=0.39, relwidth=0.05, relheight=0.04)
        
        self.create_label(
            text=self.texts.DIARY_AFTER_TEXT,
            width_ratio=0.06, height_ratio=0.03, y_ratio=0.39, x_ratio=start_x + 0.13,
            font_config=self.styles.FONTS["label_small"]
        )
        
        self.mood_after_var = tk.IntVar(value=self.styles.DIARY_CONFIG.get("default_mood", 3) + 1)
        mood_after_spinbox = tk.Spinbox(
            self.canvas, from_=1, to=5, textvariable=self.mood_after_var,
            font=self.styles.DIARY_SPINBOX_FONT, justify="center", width=3, state="readonly"
        )
        mood_after_spinbox.place(relx=start_x + 0.21, rely=0.39, relwidth=0.05, relheight=0.04)
        
        self.create_label(
            text=self.texts.DIARY_BEFORE_TEXT,
            width_ratio=0.05, height_ratio=0.03, y_ratio=0.39, x_ratio=start_x + 0.40,
            font_config=self.styles.FONTS["label_small"]
        )
        
        self.energy_before_var = tk.IntVar(value=self.styles.DIARY_CONFIG.get("default_energy", 3))
        energy_before_spinbox = tk.Spinbox(
            self.canvas, from_=1, to=5, textvariable=self.energy_before_var,
            font=self.styles.DIARY_SPINBOX_FONT, justify="center", width=3, state="readonly"
        )
        energy_before_spinbox.place(relx=start_x + 0.46, rely=0.39, relwidth=0.05, relheight=0.04)
        
        self.create_label(
            text=self.texts.DIARY_AFTER_TEXT,
            width_ratio=0.06, height_ratio=0.03, y_ratio=0.39, x_ratio=start_x + 0.53,
            font_config=self.styles.FONTS["label_small"]
        )
        
        self.energy_after_var = tk.IntVar(value=self.styles.DIARY_CONFIG.get("default_energy", 3) + 1)
        energy_after_spinbox = tk.Spinbox(
            self.canvas, from_=1, to=5, textvariable=self.energy_after_var,
            font=self.styles.DIARY_SPINBOX_FONT, justify="center", width=3, state="readonly"
        )
        energy_after_spinbox.place(relx=start_x + 0.61, rely=0.39, relwidth=0.05, relheight=0.04)
    
    def _create_notes_input(self):
        """Создание поля для заметок"""
        self.create_label(
            text=self.texts.DIARY_NOTES_TITLE,
            width_ratio=0.3, height_ratio=0.04, y_ratio=0.46,
            font_config=self.styles.FONTS["label_title"]
        )
        
        self.notes_text = tk.Text(self.canvas, font=self.styles.DIARY_NOTES_FONT, wrap="word", height=3)
        self.notes_text.place(relx=0.15, rely=0.51, relwidth=0.7, relheight=0.12)
    
    def _load_existing_entry(self, entry: Dict):
        """Загрузка существующей записи для редактирования"""
        if entry.get("practices") and len(entry["practices"]) > 0:
            practice = entry["practices"][-1]
            self.technique_var.set(practice.get("technique", self.texts.DIARY_TECHNIQUES[0]))
            level = practice.get("level", "beginner")
            self.level_var.set(self.texts.DIARY_LEVEL_BEGINNER if level == "beginner" else self.texts.DIARY_LEVEL_ADVANCED)
            self.duration_var.set(practice.get("duration", self.styles.DIARY_CONFIG.get("default_duration", 10)))
        
        if "mood_before" in entry:
            self.mood_before_var.set(entry["mood_before"])
        if "mood_after" in entry:
            self.mood_after_var.set(entry["mood_after"])
        if "energy_before" in entry:
            self.energy_before_var.set(entry["energy_before"])
        if "energy_after" in entry:
            self.energy_after_var.set(entry["energy_after"])
        if "notes" in entry:
            self.notes_text.insert("1.0", entry["notes"])
    
    def _create_save_buttons(self):
        """Создание кнопок сохранения и отмены"""
        buttons_total_width = 0.35
        buttons_start_x = (1 - buttons_total_width) / 2
        
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("save", "Сохранить запись"),
            command=self._save_entry,
            width_ratio=0.15, height_ratio=0.05, y_ratio=0.67, x_ratio=buttons_start_x,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: self.controller.show_frame("DiaryViewPage"),
            width_ratio=0.15, height_ratio=0.05, y_ratio=0.67, x_ratio=buttons_start_x + 0.18,
            font_config=self.styles.FONTS["button"]
        )
    
    def _save_entry(self):
        """Сохранение записи"""
        technique = self.technique_var.get().strip()
        duration = self.duration_var.get()
        level_text = self.level_var.get()
        notes = self.notes_text.get("1.0", "end-1c").strip()
        
        level = "beginner" if level_text == self.texts.DIARY_LEVEL_BEGINNER else "advanced"
        
        current_date = self.edit_date if self.edit_date else date.today().strftime("%Y-%m-%d")
        existing_entry = self.controller.get_diary_entry_by_date(current_date)
        
        if existing_entry:
            existing_practices = existing_entry.get("practices", [])
            updated_practices = existing_practices + [{
                "technique": technique,
                "duration": duration,
                "level": level,
                "notes": notes
            }]
            
            all_mood_before = []
            all_mood_after = []
            all_energy_before = []
            all_energy_after = []
            
            if "mood_before_list" in existing_entry and existing_entry["mood_before_list"]:
                all_mood_before = existing_entry["mood_before_list"].copy()
                all_mood_after = existing_entry["mood_after_list"].copy()
                all_energy_before = existing_entry["energy_before_list"].copy()
                all_energy_after = existing_entry["energy_after_list"].copy()
            elif "mood_before" in existing_entry:
                all_mood_before.append(existing_entry["mood_before"])
                all_mood_after.append(existing_entry["mood_after"])
                all_energy_before.append(existing_entry["energy_before"])
                all_energy_after.append(existing_entry["energy_after"])
            
            all_mood_before.append(self.mood_before_var.get())
            all_mood_after.append(self.mood_after_var.get())
            all_energy_before.append(self.energy_before_var.get())
            all_energy_after.append(self.energy_after_var.get())
            
            avg_mood_before = sum(all_mood_before) / len(all_mood_before)
            avg_mood_after = sum(all_mood_after) / len(all_mood_after)
            avg_energy_before = sum(all_energy_before) / len(all_energy_before)
            avg_energy_after = sum(all_energy_after) / len(all_energy_after)
            
            all_notes = "\n".join([p.get("notes", "") for p in updated_practices if p.get("notes")])
            
            entry = {
                "date": current_date,
                "practices": updated_practices,
                "mood_before": avg_mood_before,
                "mood_after": avg_mood_after,
                "energy_before": avg_energy_before,
                "energy_after": avg_energy_after,
                "mood_before_list": all_mood_before,
                "mood_after_list": all_mood_after,
                "energy_before_list": all_energy_before,
                "energy_after_list": all_energy_after,
                "notes": all_notes
            }
        else:
            entry = {
                "date": current_date,
                "practices": [{
                    "technique": technique,
                    "duration": duration,
                    "level": level,
                    "notes": notes
                }],
                "mood_before": self.mood_before_var.get(),
                "mood_after": self.mood_after_var.get(),
                "energy_before": self.energy_before_var.get(),
                "energy_after": self.energy_after_var.get(),
                "mood_before_list": [self.mood_before_var.get()],
                "mood_after_list": [self.mood_after_var.get()],
                "energy_before_list": [self.energy_before_var.get()],
                "energy_after_list": [self.energy_after_var.get()],
                "notes": notes
            }
        
        self.controller.add_diary_entry(entry)
        self.controller.show_frame("DiaryViewPage")


class DiaryEditPage(DiaryAddPage):
    """Страница редактирования записи дневника"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        edit_date = getattr(controller, 'edit_diary_date', None)
        super().__init__(parent, controller, bg_image, edit_date=edit_date)


class DiaryStatisticsPage(PageWithBackground):
    """Страница статистики дневника"""
    
    def __init__(self, parent: tk.Widget, controller: 'AppController', bg_image):
        super().__init__(parent, controller, bg_image)
        
        self.current_period = self.styles.DIARY_CONFIG.get("default_period", 30)
        
        self.create_title(self.texts.DIARY_TITLES.get("statistics", "📊 Статистика практик"), y_ratio=0.03)
        self._create_period_buttons()
        self._create_stats_labels()
        self._create_navigation_buttons()
        self.update_stats(30)
    
    def _create_period_buttons(self):
        """Создание кнопок выбора периода"""
        periods = [
            (self.texts.DIARY_PERIODS.get("7_days", "7 дней"), 7),
            (self.texts.DIARY_PERIODS.get("30_days", "30 дней"), 30),
            (self.texts.DIARY_PERIODS.get("90_days", "90 дней"), 90),
            (self.texts.DIARY_PERIODS.get("year", "Год"), 365)
        ]
        
        button_width = 0.08
        gap = 0.02
        total_width = len(periods) * button_width + (len(periods) - 1) * gap
        start_x = (1 - total_width) / 2
        
        for i, (text, days) in enumerate(periods):
            self.create_button(
                text=text, command=lambda d=days: self.update_stats(d),
                width_ratio=button_width, height_ratio=0.03, y_ratio=0.11,
                x_ratio=start_x + i * (button_width + gap),
                font_config=self.styles.DIARY_PERIOD_BUTTON_FONT
            )
    
    def _create_stats_labels(self):
        """Создание меток для статистики"""
        self.stats_label = self.create_rounded_label(
            text="", width_ratio=0.7, height_ratio=0.3, y_ratio=0.17,
            bg_color=self.styles.SURVEY_COLORS["description_bg"],
            font_config=self.styles.DIARY_STATS_PAGE_FONT,
            border_radius=self.styles.SURVEY_BORDER_RADIUS, justify="left"
        )
        
        self.details_label = self.create_rounded_label(
            text="", width_ratio=0.4, height_ratio=0.1, y_ratio=0.50,
            bg_color=self.styles.SURVEY_COLORS["label_bg"],
            font_config=self.styles.DIARY_STATS_PAGE_FONT,
            border_radius=self.styles.SURVEY_BORDER_RADIUS, justify="left"
        )
    
    def _create_navigation_buttons(self):
        """Создание кнопок навигации"""
        self.create_button(
            text=self.texts.DIARY_BUTTONS.get("back_to_diary", "К записям"),
            command=lambda: self.controller.show_frame("DiaryViewPage"),
            width_ratio=0.20, height_ratio=0.05, y_ratio=0.64,
            font_config=self.styles.FONTS["button"]
        )
        
        self.create_button(
            text=self.texts.BUTTON_TEXTS["back"],
            command=lambda: self.controller.show_frame("DiaryStartPage"),
            width_ratio=self.styles.WIDGET_SIZES["button_medium"]["width"],
            height_ratio=self.styles.WIDGET_SIZES["button_medium"]["height"],
            y_ratio=0.71
        )
    
    def update_stats(self, days: int):
        """Обновление статистики"""
        self.current_period = days
        stats = self.controller.get_diary_statistics(days)
        
        if stats and stats.total_days > 0:
            days_word = self.controller.get_day_word(stats.total_days)
            sessions_word = self.controller.get_session_word(stats.total_sessions)
            streak_word = self.controller.get_day_word(stats.current_streak)
            best_streak_word = self.controller.get_day_word(stats.best_streak)
            
            stats_text = f"{self.texts.DIARY_STATS_TITLE}\n\n{stats.total_days} {days_word} • {stats.total_sessions} {sessions_word} • {stats.total_minutes} {self.texts.DIARY_MINUTES_TEXT}\n{self.texts.DIARY_STREAK_TEXT}: {stats.current_streak} {streak_word} ({self.texts.DIARY_BEST_TEXT}: {stats.best_streak} {best_streak_word})\n\n😊 {self.texts.DIARY_MOOD_LABEL}: {stats.average_mood_before:.1f} → {stats.average_mood_after:.1f} ({stats.get_formatted_mood()})\n\n⚡ {self.texts.DIARY_ENERGY_LABEL}: {stats.average_energy_before:.1f} → {stats.average_energy_after:.1f} ({stats.get_formatted_energy()})"
            
            self.stats_label.config(text=stats_text)
            
            details_text = f"{self.texts.DIARY_POPULAR_TECHNIQUE_TEXT}\n\n"
            if stats.most_practiced_technique['name']:
                tech = stats.most_practiced_technique
                sessions_word = self.controller.get_session_word(tech['count'])
                details_text += f"{tech['name']}\n{tech['count']} {sessions_word}"
            else:
                details_text += self.texts.DIARY_NO_DATA_TEXT
            
            self.details_label.config(text=details_text)
        else:
            self.stats_label.config(text=self.texts.DIARY_NO_DATA_TEXT)
            self.details_label.config(text=self.texts.DIARY_NO_DATA_TEXT)
