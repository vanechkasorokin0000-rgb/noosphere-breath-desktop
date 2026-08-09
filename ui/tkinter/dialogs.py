"""
Кастомные диалоговые окна и всплывающие подсказки
"""

import tkinter as tk
from PIL import Image, ImageTk
from typing import Optional, List, Dict, Any

from .styles import styles, TkinterStyles


class ToolTip:
    """Класс для создания всплывающих аннотаций"""
    
    def __init__(self, widget: tk.Widget, text: str, style: Optional[TkinterStyles] = None):
        self.widget = widget
        self.text = text
        self.style = style or styles
        self.config = self.style.TOOLTIP_CONFIG
        self.tip_window = None
        self.show_timer = None
        self.hide_timer = None
        
        self.widget.bind('<Enter>', self._schedule_show)
        self.widget.bind('<Leave>', self._schedule_hide)
        self.widget.bind('<Button-1>', self._hide_tip)
    
    def _schedule_show(self, event=None):
        self._cancel_timers()
        delay = self.config.get("delay", 500)
        self.show_timer = self.widget.after(delay, self._show_tip)
    
    def _schedule_hide(self, event=None):
        self._cancel_timers()
        self.hide_timer = self.widget.after(100, self._hide_tip)
    
    def _cancel_timers(self):
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None
    
    def _show_tip(self):
        self._hide_tip()
        if not self.text:
            return
        
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        
        frame = tk.Frame(
            self.tip_window, bg=self.config.get("border_color", "#D4A574"),
            bd=self.config.get("border_width", 2), relief="solid"
        )
        frame.pack(fill="both", expand=True)
        
        label = tk.Label(
            frame, text=self.text, justify="left",
            bg=self.config.get("bg_color", "#FFF8DC"), fg=self.config.get("fg_color", "#333333"),
            font=(self.config["font"]["family"], self.config["font"]["size"], self.config["font"]["weight"]),
            padx=self.config.get("padding_x", 10), pady=self.config.get("padding_y", 8)
        )
        label.pack()
        
        self.tip_window.update_idletasks()
        
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + self.config.get("offset_x", 20)
        y = self.widget.winfo_rooty() + self.config.get("offset_y", 0)
        
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
        tip_width = self.tip_window.winfo_width()
        tip_height = self.tip_window.winfo_height()
        
        if x + tip_width > screen_width:
            x = self.widget.winfo_rootx() - tip_width - self.config.get("offset_x", 20)
        if y + tip_height > screen_height:
            y = screen_height - tip_height
        if y < 0:
            y = 0
        
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.bind('<Enter>', self._cancel_hide)
        self.tip_window.bind('<Leave>', self._schedule_hide)
    
    def _cancel_hide(self, event=None):
        if self.hide_timer:
            self.widget.after_cancel(self.hide_timer)
            self.hide_timer = None
    
    def _hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
        self._cancel_timers()


class CustomDialog(tk.Toplevel):
    """Кастомное модальное диалоговое окно с масштабированием"""
    
    def __init__(self, parent: tk.Widget, title: str, message: str,
                 button_texts: List[str] = ["OK", "Отмена"], default_button: int = 0,
                 bg_image: Optional[Image.Image] = None):
        super().__init__(parent)
        
        self.parent = parent
        self.result = None
        self.bg_image = bg_image
        self.button_texts = button_texts
        self.default_button = default_button
        
        # Получаем стили
        if hasattr(parent, 'styles'):
            self.style = parent.styles
        else:
            self.style = styles
        
        self.config = self.style.DIALOG_CONFIG
        
        self.title(title)
        if self.config.get("modal", True):
            self.transient(parent)
            self.grab_set()
        
        self.overrideredirect(True)
        self.update_idletasks()
        
        self._setup_ui(message)
        self.bind("<Configure>", self._on_configure)
        self.center_window()
        
        if self.config.get("close_on_escape", True):
            self.bind("<Escape>", lambda e: self.close())
        
        if self.config.get("enable_animation", False):
            self.attributes("-alpha", 0)
            self._animate_fade_in()
        
        if hasattr(self, 'buttons') and self.buttons and default_button < len(self.buttons):
            self.buttons[default_button].focus_set()
    
    def _setup_ui(self, message: str):
        """Создание UI диалога"""
        bg_color = self.config.get("bg_color", "#FFF8DC")
        
        self.container = tk.Frame(self, bg=bg_color)
        self.container.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.container, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.content_frame = tk.Frame(self.canvas, bg=bg_color)
        
        # Заголовок
        title_font = self._calculate_scaled_font(self.config["title_font"])
        self.title_label = tk.Label(
            self.content_frame, text=self.title(), font=title_font,
            bg=bg_color, fg=self.config.get("title_fg_color", "#000000")
        )
        
        # Сообщение
        msg_font = self._calculate_scaled_font(self.config["message_font"])
        self.message_label = tk.Label(
            self.content_frame, text=message, font=msg_font,
            bg=bg_color, fg=self.config.get("message_fg_color", "#333333"),
            justify="center", wraplength=400
        )
        
        # Кнопки
        button_frame = tk.Frame(self.content_frame, bg=bg_color)
        self.buttons = []
        button_font = self._calculate_scaled_font(self.config["button_font"])
        
        for i, text in enumerate(self.button_texts):
            btn = tk.Button(
                button_frame, text=text, font=button_font,
                bg=self.config.get("button_bg_color", "#F0FFFF"),
                fg=self.config.get("button_fg_color", "#000000"),
                command=lambda idx=i: self._button_click(idx),
                width=self.config.get("button_width", 10), cursor="hand2"
            )
            btn.pack(side="left", padx=self.config.get("button_padx", 10))
            self.buttons.append(btn)
        
        self.title_label.pack(pady=self.config.get("title_pady", 15))
        self.message_label.pack(pady=self.config.get("message_pady", 10),
                                padx=self.config.get("message_padx", 20),
                                expand=True, fill="both")
        button_frame.pack(pady=self.config.get("button_pady", 15))
        
        self._update_content_frame_position()
    
    def _update_content_frame_position(self):
        """Обновление позиции content_frame"""
        if hasattr(self, 'dialog_width') and hasattr(self, 'dialog_height'):
            padding_x = self.config.get("content_padding_x", 0.05)
            padding_y = self.config.get("content_padding_y", 0.05)
            self.content_frame.place(
                relx=padding_x, rely=padding_y,
                relwidth=1 - 2*padding_x, relheight=1 - 2*padding_y
            )
    
    def center_window(self):
        """Центрирование окна"""
        self.update_idletasks()
        
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = int(parent_width * self.config.get("width_ratio", 0.4))
        dialog_height = int(parent_height * self.config.get("height_ratio", 0.3))
        dialog_width = max(dialog_width, self.config.get("min_width", 300))
        dialog_height = max(dialog_height, self.config.get("min_height", 200))
        
        x = self.parent.winfo_rootx() + (parent_width - dialog_width) // 2
        y = self.parent.winfo_rooty() + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.dialog_width = dialog_width
        self.dialog_height = dialog_height
        
        self._update_content_frame_position()
        self._update_widget_sizes()
    
    def _calculate_scaled_font(self, font_config: Dict[str, Any]) -> tuple:
        """Расчет масштабированного шрифта"""
        if not font_config.get("scale_with_window", True):
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        if not hasattr(self, 'dialog_width'):
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        scale_factor = self.dialog_width / self.style.BASE_WINDOW_WIDTH
        base_size = font_config.get("size", 16)
        scaled_size = int(base_size * scale_factor)
        min_size = font_config.get("min_size", base_size // 2)
        max_size = font_config.get("max_size", base_size * 2)
        final_size = max(min_size, min(scaled_size, max_size))
        
        return (font_config["family"], final_size, font_config.get("weight", "normal"))
    
    def _update_widget_sizes(self):
        """Обновление размеров виджетов"""
        if not self.winfo_exists():
            return
        
        if hasattr(self, 'message_label') and self.message_label.winfo_exists():
            self.message_label.config(wraplength=int(self.dialog_width * 0.7))
        
        for widget, font_config in [
            (self.title_label, self.config["title_font"]),
            (self.message_label, self.config["message_font"])
        ]:
            if widget and widget.winfo_exists():
                new_font = self._calculate_scaled_font(font_config)
                widget.config(font=new_font)
        
        for button in self.buttons:
            if button.winfo_exists():
                new_font = self._calculate_scaled_font(self.config["button_font"])
                button.config(font=new_font)
    
    def _update_background(self):
        """Обновление фона"""
        if self.bg_image and self.canvas.winfo_exists():
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            if width > 1 and height > 1:
                try:
                    resized = self.bg_image.resize((width, height), Image.LANCZOS)
                    self.bg_photo = ImageTk.PhotoImage(resized)
                    self.canvas.delete("background")
                    self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
                except Exception as e:
                    print(f"Ошибка обновления фона: {e}")
    
    def _on_configure(self, event):
        self.dialog_width = event.width
        self.dialog_height = event.height
        self._update_background()
        self._update_content_frame_position()
        self._update_widget_sizes()
    
    def _on_canvas_configure(self, event):
        self._update_background()
    
    def _animate_fade_in(self, step: int = 0):
        steps = self.config.get("animation_steps", 10)
        if step <= steps:
            self.attributes("-alpha", step / steps)
            self.after(self.config.get("animation_delay", 30), lambda: self._animate_fade_in(step + 1))
    
    def _button_click(self, index: int):
        self.result = index
        self.close()
    
    def close(self):
        if self.config.get("enable_animation", False):
            self._animate_fade_out()
        else:
            self.grab_release()
            self.destroy()
    
    def _animate_fade_out(self, step: int = None):
        steps = self.config.get("animation_steps", 10)
        if step is None:
            step = steps
        if step >= 0:
            self.attributes("-alpha", step / steps)
            self.after(self.config.get("animation_delay", 30), lambda: self._animate_fade_out(step - 1))
        else:
            self.grab_release()
            self.destroy()
    
    def show(self) -> Optional[str]:
        """Показать диалог и вернуть результат"""
        self.wait_window()
        if self.result is not None:
            return self.button_texts[self.result]
        return None
