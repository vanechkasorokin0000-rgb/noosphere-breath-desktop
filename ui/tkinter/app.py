import tkinter as tk
from tkinter import messagebox
import pygame
import os
import sys
from PIL import Image
from typing import Dict, Type

from core.app_controller import AppController
from core.protection_simple import AppProtection
from .styles import styles
from .base_page import PageWithBackground

import texts as texts_ru
import texts_en


class ActivationScreen(tk.Frame):
    """Экран активации для Tkinter"""
    
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        self.configure(bg="#0D0D26")
        
        # Заголовок
        title = tk.Label(self, text="Noosphere Breath", font=("Arial", 32, "bold"),
                        bg="#0D0D26", fg="white")
        title.pack(pady=40)
        
        desc = tk.Label(self, text="Введите ключ активации из 16 цифр",
                       font=("Arial", 16), bg="#0D0D26", fg="#CCCCCC")
        desc.pack(pady=10)
        
        # Поле ввода
        self.key_var = tk.StringVar()
        self.key_entry = tk.Entry(self, textvariable=self.key_var, font=("Arial", 20),
                                  justify="center", width=22)
        self.key_entry.pack(pady=20)
        
        # Кнопка
        self.btn = tk.Button(self, text="Активировать", font=("Arial", 18),
                             bg="#2E7D32", fg="white", padx=30, pady=10,
                             command=self._activate)
        self.btn.pack(pady=20)
        
        self.pack(expand=True)
    
    def _activate(self):
        key = self.key_var.get().strip().replace("-", "")
        if len(key) < 16:
            messagebox.showerror("Ошибка", "Ключ должен содержать 16 цифр")
            return
        
        success, message = self.app.activate_with_key(key)
        if success:
            messagebox.showinfo("Успех", message)
            self.app.show_main_screen()
        else:
            messagebox.showerror("Ошибка", message)


class TkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.controller = AppController()
        self.controller.initialize(texts_ru, texts_en)
        self.controller.set_app_instance(self)
        
        self.protection = AppProtection()
        self.activation_required = not self.protection.is_activated()
        
        self.title("Noosphere Breath")
        self.geometry("1200x800")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self._exit_fullscreen)
        self.bind("<Configure>", self._on_resize)
        
        pygame.mixer.init()
        self.bg_image = self._load_image("resources/background21.png")
        self.styles = styles
        
        self.controller.register_callback("language_changed", self._on_language_changed)
        self.controller.register_callback("cleanup", self.cleanup)
        self.controller.register_callback("show_frame", self.show_frame)
        
        self.page_classes: Dict[str, Type[PageWithBackground]] = {}
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        
        if self.activation_required:
            self._show_activation()
        else:
            self.show_main_screen()
    
    def activate_with_key(self, key: str) -> tuple:
        return self.protection.activate(key)
    
    def _show_activation(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ActivationScreen(self.container, self.controller, self)
    
    def show_main_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.show_frame("StartPage")
    
    def register_page(self, name: str, page_class: Type[PageWithBackground]):
        self.page_classes[name] = page_class
    
    def show_frame(self, page_name: str):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        frame_class = self.page_classes.get(page_name)
        if frame_class is None:
            return
        
        try:
            self.current_frame = frame_class(self.container, self.controller, self.bg_image)
            self.current_frame.pack(fill="both", expand=True)
            self.update_idletasks()
            if hasattr(self.current_frame, 'update_background'):
                self.current_frame.update_background()
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _on_language_changed(self, texts_module):
        pass
    
    def _exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)
    
    def _on_resize(self, event):
        pass
    
    def _load_image(self, path: str):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        full_path = os.path.join(base_path, path)
        if not os.path.exists(full_path):
            return Image.new('RGB', (1920, 1080), color='#F0FFFF')
        return Image.open(full_path)
    
    def cleanup(self):
        pygame.mixer.quit()
        self.destroy()
    
    def run(self):
        self.show_frame("StartPage")
        self.mainloop()
