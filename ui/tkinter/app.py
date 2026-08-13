import tkinter as tk
from tkinter import messagebox
import pygame
import os
import sys
from PIL import Image
from typing import Dict, Type

from core.app_controller import AppController
from core.protection_simple import AppProtection
from activation_screen import ActivationScreen
from .styles import styles
from .base_page import PageWithBackground

import texts as texts_ru
import texts_en


class TkinterApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.controller = AppController()
        self.controller.initialize(texts_ru, texts_en)
        self.controller.set_app_instance(self)
        
        self.protection = AppProtection()
        print("DEBUG: Checking activation...")
        self.activation_required = not self.protection.is_activated()
        print(f"DEBUG: is_activated={self.protection.is_activated()}, activation_required={self.activation_required}")
        
        self.title("Noosphere Breath")
        try:
            import sys
            if getattr(sys, 'frozen', False):
                # PyInstaller bundle
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_path, "resources", "icon.png")
            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                self.icon_img = ImageTk.PhotoImage(Image.open(icon_path))
                self.iconphoto(True, self.icon_img)
        except Exception as e:
            print(f"Иконка не загружена: {e}")
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
        self.geometry("1200x800")
    
    def _on_resize(self, event):
        pass
    
    def _load_image(self, path: str):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        # Ищем в нескольких местах
        candidates = [
            os.path.join(base_path, path),
            os.path.join(base_path, "resources", path),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", path),
        ]
        for full_path in candidates:
            if os.path.exists(full_path):
                return Image.open(full_path)
        return Image.new('RGB', (1920, 1080), color='#F0FFFF')
    
    def cleanup(self):
        pygame.mixer.quit()
        self.destroy()
    
    def run(self):
        if self.activation_required:
            self._show_activation()
        else:
            self.show_frame("StartPage")
        self.mainloop()
