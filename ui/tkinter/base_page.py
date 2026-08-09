"""
Базовый класс для всех страниц с фоновым изображением
"""

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from typing import Optional, Callable, Dict, Any

from core.app_controller import AppController
from .styles import styles
from .dialogs import ToolTip


class PageWithBackground(tk.Frame):
    """Базовый класс для всех страниц с фоновым изображением"""
    
    def __init__(self, parent: tk.Widget, controller: AppController, bg_image: Image.Image):
        super().__init__(parent)
        self.controller = controller
        self.texts = controller.get_texts()
        self.styles = styles
        self.original_bg_image = bg_image
        self.widgets = []
        self._bg_cache = {}
        self._cache_maxsize = 5
        
        # Список для хранения ВСЕХ ссылок на PhotoImage (защита от GC)
        self._all_images = []

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=self.styles.COLORS["canvas_bg"])
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Configure>", self._on_configure)
        
        self.update_idletasks()
    
    def _on_configure(self, event: tk.Event):
        """Обработка изменения размера окна"""
        if not self.canvas.winfo_exists():
            return
        self.update_background()
        self.update_widget_sizes_and_positions()

    def update_background(self):
        """Обновление фонового изображения"""
        self.update_idletasks()
        
        if not self.canvas.winfo_exists():
            return
            
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width > 1 and height > 1:
            try:
                cache_key = (width, height)
                
                if cache_key in self._bg_cache:
                    new_photo = self._bg_cache[cache_key]
                else:
                    if len(self._bg_cache) >= self._cache_maxsize:
                        oldest_key = next(iter(self._bg_cache))
                        self._bg_cache.pop(oldest_key)
                    
                    resized = self.original_bg_image.resize((width, height), Image.LANCZOS)
                    new_photo = ImageTk.PhotoImage(resized)
                    self._bg_cache[cache_key] = new_photo
                    self._all_images.append(new_photo)
                
                self.bg_photo = new_photo
                self.canvas.delete("background")
                self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")

            except Exception as e:
                print(f"Ошибка при обновлении фона: {e}")

    def calculate_scaled_font(self, font_config: Dict[str, Any]) -> tuple:
        """Расчет масштабированного шрифта"""
        if not font_config.get("scale_with_window", True):
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        current_width = self.canvas.winfo_width()
        current_height = self.canvas.winfo_height()
        
        if current_width <= 1 or current_height <= 1:
            return (font_config["family"], font_config["size"], font_config.get("weight", "normal"))
        
        scale_factor = min(
            current_width / self.styles.BASE_WINDOW_WIDTH,
            current_height / self.styles.BASE_WINDOW_HEIGHT
        )
        
        base_size = font_config["size"]
        scaled_size = int(base_size * scale_factor)
        
        min_size = font_config.get("min_size", base_size // 2)
        max_size = font_config.get("max_size", base_size * 2)
        final_size = max(min_size, min(scaled_size, max_size))
        
        return (font_config["family"], final_size, font_config.get("weight", "normal"))

    def _save_image_ref(self, photo: ImageTk.PhotoImage):
        """Сохраняет ссылку на PhotoImage для защиты от сборщика мусора"""
        self._all_images.append(photo)
        return photo

    def create_widget_image(self, width: int, height: int, bg_color: str) -> ImageTk.PhotoImage:
        """Создание обычного изображения для фона виджета"""
        if width <= 0 or height <= 0:
            width, height = 1, 1
        img = Image.new("RGBA", (width, height), bg_color)
        photo = ImageTk.PhotoImage(img)
        self._save_image_ref(photo)
        return photo

    def create_rounded_image(self, width: int, height: int, bg_color: str, radius: int = 20) -> ImageTk.PhotoImage:
        """Создание изображения со скругленными углами"""
        if width <= 0 or height <= 0:
            width, height = 1, 1
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=bg_color)
        photo = ImageTk.PhotoImage(img)
        self._save_image_ref(photo)
        return photo

    def add_widget(self, widget: tk.Widget, width_ratio: float, height_ratio: float, 
                   y_ratio: float, x_ratio: Optional[float] = None):
        """Добавление виджета для автоматического управления"""
        widget.width_ratio = width_ratio
        widget.height_ratio = height_ratio
        widget.y_ratio = y_ratio
        widget.x_ratio = x_ratio
        self.place_widget(widget)
        self.widgets.append(widget)

    def place_widget(self, widget: tk.Widget):
        """Размещение виджета на canvas"""
        if not widget.winfo_exists():
            return
            
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            widget_width = int(canvas_width * widget.width_ratio)
            widget_height = int(canvas_height * widget.height_ratio)
            
            if hasattr(widget, 'x_ratio') and widget.x_ratio is not None:
                x = canvas_width * widget.x_ratio
            else:
                x = (canvas_width - widget_width) / 2
                
            y = canvas_height * widget.y_ratio
            
            try:
                widget.place(x=x, y=y, width=widget_width, height=widget_height, anchor="nw")
            except tk.TclError:
                pass

    def update_widget_sizes_and_positions(self):
        """Обновление размеров и позиций всех виджетов"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            return
            
        for widget in self.widgets:
            if not widget.winfo_exists():
                continue
                
            # Обработка Text-виджетов со скроллингом
            if isinstance(widget, tk.Text):
                if hasattr(widget, '_frame') and widget._frame.winfo_exists():
                    widget._frame.place(
                        relx=widget.x_ratio if hasattr(widget, 'x_ratio') and widget.x_ratio is not None else (1 - widget.width_ratio) / 2,
                        rely=widget.y_ratio,
                        relwidth=widget.width_ratio,
                        relheight=widget.height_ratio
                    )
                
                if hasattr(widget, 'font_config'):
                    new_font = self.calculate_scaled_font(widget.font_config)
                    try:
                        widget.config(font=new_font)
                    except tk.TclError:
                        pass
                continue
            
            # Стандартная обработка: позиционирование
            self.place_widget(widget)
            
            # Обновление изображения фона под новый размер
            if hasattr(widget, 'bg_color'):
                widget_width = int(canvas_width * widget.width_ratio)
                widget_height = int(canvas_height * widget.height_ratio)
                
                if widget_width > 0 and widget_height > 0:
                    if hasattr(widget, 'border_radius'):
                        new_image = self.create_rounded_image(
                            widget_width, widget_height, widget.bg_color, widget.border_radius
                        )
                    else:
                        new_image = self.create_widget_image(widget_width, widget_height, widget.bg_color)
                    
                    widget.image = new_image
                    try:
                        widget.configure(image=new_image)
                    except tk.TclError:
                        pass
            
            # Обновление шрифта
            if hasattr(widget, 'font_config'):
                new_font = self.calculate_scaled_font(widget.font_config)
                try:
                    widget.config(font=new_font)
                except tk.TclError:
                    pass
                
                if hasattr(widget, 'wrap_ratio'):
                    widget_width = int(canvas_width * widget.width_ratio)
                    try:
                        widget.config(wraplength=int(widget_width * widget.wrap_ratio))
                    except tk.TclError:
                        pass

    def create_scrollable_label(self, text: str, width_ratio: float, height_ratio: float, y_ratio: float,
                                 x_ratio: Optional[float] = None, bg_color: Optional[str] = None,
                                 text_color: Optional[str] = None, font_config: Optional[Dict] = None,
                                 justify: str = "left", border_radius: int = 0) -> tk.Text:
        """
        Создание текстовой метки со скроллингом.
        Возвращает Text виджет для возможности обновления текста.
        """
        if bg_color is None:
            bg_color = self.styles.COLORS["label_bg"]
        if text_color is None:
            text_color = self.styles.COLORS["label_fg"]
        if font_config is None:
            font_config = self.styles.FONTS["label_medium"]
        
        font = self.calculate_scaled_font(font_config)
        
        text_frame = tk.Frame(self.canvas, bg=bg_color)
        
        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=font,
            bg=bg_color,
            fg=text_color,
            padx=20,
            pady=15,
            spacing1=5,
            spacing2=2,
            spacing3=5,
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        text_widget.insert("1.0", text)

        # Настройка тегов для выравнивания
        text_widget.tag_configure("center", justify="center")
        text_widget.tag_configure("left", justify="left")
        text_widget.tag_configure("right", justify="right")
    
        # Применяем тег ко всему тексту
        text_widget.tag_add(justify, "1.0", "end")
    
        text_widget.configure(state="disabled")
        
        scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=text_widget.yview,
            bg="#D4A574",
            troughcolor=bg_color,
            activebackground="#C4A474"
        )
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_widget.pack(side="left", fill="both", expand=True)
        
        text_widget.font_config = font_config
        text_widget.width_ratio = width_ratio
        text_widget.height_ratio = height_ratio
        text_widget.y_ratio = y_ratio
        text_widget.x_ratio = x_ratio
        text_widget._frame = text_frame
        text_widget._justify = justify  # Сохраняем для последующего использования
        
        text_frame.place(
            relx=x_ratio if x_ratio is not None else (1 - width_ratio) / 2,
            rely=y_ratio,
            relwidth=width_ratio,
            relheight=height_ratio
        )
        
        self.widgets.append(text_widget)
        
        
        return text_widget
    

    def create_button(self, text: str, command: Callable, width_ratio: float, height_ratio: float,
                      y_ratio: float, x_ratio: Optional[float] = None, bg_color: Optional[str] = None,
                      text_color: Optional[str] = None, font_config: Optional[Dict] = None) -> tk.Button:
        """Создание кнопки"""
        if bg_color is None:
            bg_color = self.styles.COLORS["button_bg"]
        if text_color is None:
            text_color = self.styles.COLORS["button_fg"]
        if font_config is None:
            font_config = self.styles.FONTS["button"]
            
        font = self.calculate_scaled_font(font_config)
        
        img = self.create_widget_image(100, 50, bg_color)
        
        button = tk.Button(
            self.canvas, text=text, image=img, compound="center",
            fg=text_color, font=font, command=command,
            anchor="center", justify="center", relief="flat", borderwidth=0,
            activebackground=bg_color
        )
        button.image = img
        button.config(cursor="hand2")
        button.font_config = font_config
        button.bg_color = bg_color
        button.wrap_ratio = self.styles.TEXT_WRAP["button"]
        
        self.add_widget(button, width_ratio, height_ratio, y_ratio, x_ratio)
        return button

    def create_label(self, text: str, width_ratio: float, height_ratio: float, y_ratio: float,
                     x_ratio: Optional[float] = None, bg_color: Optional[str] = None,
                     text_color: Optional[str] = None, font_config: Optional[Dict] = None,
                     justify: str = "left") -> tk.Label:
        """Создание текстовой метки"""
        if bg_color is None:
            bg_color = self.styles.COLORS["label_bg"]
        if text_color is None:
            text_color = self.styles.COLORS["label_fg"]
        if font_config is None:
            font_config = self.styles.FONTS["label_medium"]
            
        font = self.calculate_scaled_font(font_config)
        
        img = self.create_widget_image(100, 50, bg_color)
        
        label = tk.Label(
            self.canvas, text=text, image=img, compound="center",
            fg=text_color, font=font, justify=justify, anchor="nw"
        )
        label.image = img
        label.font_config = font_config
        label.bg_color = bg_color
        label.wrap_ratio = self.styles.TEXT_WRAP["label"]
        
        self.add_widget(label, width_ratio, height_ratio, y_ratio, x_ratio)
        return label

    def create_rounded_label(self, text: str, width_ratio: float, height_ratio: float, y_ratio: float,
                             x_ratio: Optional[float] = None, bg_color: Optional[str] = None,
                             text_color: Optional[str] = None, font_config: Optional[Dict] = None,
                             justify: str = "center", border_radius: int = 20) -> tk.Label:
        """Создание текстовой метки со скругленными углами"""
        if bg_color is None:
            bg_color = self.styles.SURVEY_COLORS["label_bg"]
        if text_color is None:
            text_color = self.styles.SURVEY_COLORS["label_fg"]
        if font_config is None:
            font_config = self.styles.FONTS["label_medium"]
            
        font = self.calculate_scaled_font(font_config)
        img = self.create_rounded_image(100, 50, bg_color, border_radius)
        
        label = tk.Label(
            self.canvas, text=text, image=img, compound="center",
            fg=text_color, font=font, justify=justify, anchor="center", padx=20, pady=10
        )
        label.image = img
        label.font_config = font_config
        label.bg_color = bg_color
        label.border_radius = border_radius
        label.wrap_ratio = self.styles.TEXT_WRAP["label"]
        
        self.add_widget(label, width_ratio, height_ratio, y_ratio, x_ratio)
        return label

    def create_title(self, text: str, width_ratio: Optional[float] = None,
                     height_ratio: Optional[float] = None, y_ratio: float = 0.05,
                     x_ratio: Optional[float] = None) -> tk.Label:
        """Создание заголовка страницы"""
        if width_ratio is None:
            width_ratio = self.styles.WIDGET_SIZES["title"]["width"]
        if height_ratio is None:
            height_ratio = self.styles.WIDGET_SIZES["title"]["height"]
            
        return self.create_label(
            text=text, width_ratio=width_ratio, height_ratio=height_ratio,
            y_ratio=y_ratio, x_ratio=x_ratio,
            bg_color=self.styles.COLORS["title_bg"], text_color=self.styles.COLORS["title_fg"],
            font_config=self.styles.FONTS["title"], justify="center"
        )
    
    def create_button_with_tooltip(self, text: str, command: Callable, tooltip_text: str,
                                   width_ratio: float, height_ratio: float, y_ratio: float,
                                   x_ratio: Optional[float] = None, bg_color: Optional[str] = None,
                                   text_color: Optional[str] = None,
                                   font_config: Optional[Dict] = None) -> tk.Button:
        """Создание кнопки с всплывающей подсказкой"""
        button = self.create_button(text, command, width_ratio, height_ratio, y_ratio,
                                    x_ratio, bg_color, text_color, font_config)
        ToolTip(button, tooltip_text, self.styles)
        return button
    
    def destroy(self):
        """Очистка ресурсов при уничтожении страницы"""
        self._all_images.clear()
        self._bg_cache.clear()
        self.widgets.clear()
        
        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.destroy()
        
        super().destroy()
