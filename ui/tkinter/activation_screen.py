import tkinter as tk
from tkinter import messagebox

class ActivationScreen(tk.Frame):
    def __init__(self, parent, controller, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        self.max_attempts = 3
        self._load_attempts()
        self.configure(bg="#0D0D26")
        
        # Центрирующий контейнер
        container = tk.Frame(self, bg="#0D0D26")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Заголовок
        title = tk.Label(container, text="Noosphere Breath", 
                        font=("Arial", 36, "bold"), bg="#0D0D26", fg="white")
        title.pack(pady=(0, 30))
        
        # Подзаголовок
        desc = tk.Label(container, text="Введите ключ активации из 16 цифр\nФормат: XXXX-XXXX-XXXX-XXXX",
                       font=("Arial", 16), bg="#0D0D26", fg="#CCCCCC", justify="center")
        desc.pack(pady=(0, 20))
        
        # Поле ввода (большое)
        self.key_var = tk.StringVar()
        self.key_var.trace('w', self._format_key)
        self.key_entry = tk.Entry(container, textvariable=self.key_var, 
                                  font=("Arial", 24), justify="center", width=22,
                                  bg="#1A1A3E", fg="white", insertbackground="white",
                                  relief="flat", bd=2)
        self.key_entry.pack(pady=(0, 20), ipady=10)
        
        # Кнопка
        self.btn = tk.Button(container, text="Активировать", 
                            font=("Arial", 18, "bold"), bg="black", fg="white", 
                            padx=40, pady=15, relief="flat", cursor="hand2",
                            
                            command=self._activate)
        self.btn.pack(pady=(0, 30))
        
        # Подсказка
        support = tk.Label(container, text="По вопросам: @Midnightclimber\nnoosphere_project@mail.ru",
                          font=("Arial", 12), bg="#0D0D26", fg="#888888")
        support.pack()
        
        self.attempts_label = tk.Label(container, text=f"Осталось попыток: {max(0, self.max_attempts - self.attempts)}",
                                       font=("Arial", 12), bg="#0D0D26", fg="#CCCCCC")
        self.attempts_label.pack()
        
        self.pack(expand=True, fill="both")
    
    def _update_attempts_label(self):
        remaining = max(0, self.max_attempts - self.attempts)
        if hasattr(self, 'attempts_label'):
            self.attempts_label.config(text=f"Осталось попыток: {remaining}")
    
    def _load_attempts(self):
        try:
            with open('activation_attempts.txt', 'r') as f:
                self.attempts = int(f.read())
        except:
            self.attempts = 0
    
    def _save_attempts(self):
        try:
            with open('activation_attempts.txt', 'w') as f:
                f.write(str(self.attempts))
        except:
            pass
    
    def _format_key(self, *args):
        """Автоматически форматирует ввод как XXXX-XXXX-XXXX-XXXX"""
        text = ''.join(c for c in self.key_var.get() if c.isdigit())
        if len(text) > 16:
            text = text[:16]
        
        # Добавляем дефисы
        formatted = ''
        for i, c in enumerate(text):
            if i > 0 and i % 4 == 0:
                formatted += '-'
            formatted += c
        
        # Убираем рекурсивный вызов
        if formatted != self.key_var.get():
            self.key_var.set(formatted)
            # Перемещаем курсор в конец
            self.key_entry.icursor(len(formatted))
    
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
print("🔵 НОВАЯ ВЕРСИЯ activation_screen.py v2.1")
