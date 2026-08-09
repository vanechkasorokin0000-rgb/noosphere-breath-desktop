"""
Экран активации приложения
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.core.window import Window


class ActivationScreen(Screen):
    """Экран активации лицензии"""
    
    def __init__(self, controller, app_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.app = app_instance  # Ссылка на KivyApp
        self.register_event_type('on_activated')
        
        # Счетчик попыток
        self.attempts = 0
        self.max_attempts = 3
        
        self._build_ui()
    
    def _build_ui(self):
        """Построение UI"""
        # Фон
        with self.canvas.before:
            Color(0.05, 0.05, 0.15, 1)  # Темно-синий фон
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)
        
        # Основной layout
        layout = BoxLayout(
            orientation='vertical',
            padding=[dp(30), dp(40)],
            spacing=dp(20)
        )
        
        # Логотип
        title = Label(
            text="Noosphere Breath",
            font_size=sp(32),
            size_hint_y=0.12,
            color=(1, 1, 1, 1),
            bold=True,
            halign='center',
            valign='middle'
        )
        title.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        layout.add_widget(title)
        
        # Описание
        desc = Label(
            text="Для активации приложения\nвведите ключ, полученный от бота",
            font_size=sp(16),
            size_hint_y=0.1,
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
            valign='middle'
        )
        desc.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        layout.add_widget(desc)
        
        # Поле ввода ключа
        self.key_input = TextInput(
            hint_text="XXXX-XXXX-XXXX-XXXX",
            font_size=sp(20),
            size_hint_y=0.08,
            multiline=False,
            background_color=(0.15, 0.15, 0.25, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            halign='center',
            padding=[dp(10), dp(10)]
        )
        self.key_input.bind(text=self._on_key_text)
        layout.add_widget(self.key_input)
        
        # Информация о попытках
        self.attempts_label = Label(
            text=f"Осталось попыток: {self.max_attempts}",
            font_size=sp(14),
            size_hint_y=0.05,
            color=(0.8, 0.8, 0.3, 1),
            halign='center'
        )
        self.attempts_label.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        layout.add_widget(self.attempts_label)
        
        # Индикатор загрузки
        self.loading_label = Label(
            text="",
            font_size=sp(14),
            size_hint_y=0.05,
            color=(0.5, 0.8, 1, 1),
            halign='center'
        )
        self.loading_label.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        layout.add_widget(self.loading_label)
        
        # Кнопка активации
        self.activate_btn = Button(
            text="Активировать",
            font_size=sp(18),
            size_hint_y=0.08,
            background_color=(0.3, 0.6, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        self.activate_btn.bind(on_press=self._activate)
        layout.add_widget(self.activate_btn)
        
        # Информация о поддержке
        support_label = Label(
            text="По вопросам активации:\n@NoosphereBreath_bot",
            font_size=sp(12),
            size_hint_y=0.08,
            color=(0.5, 0.5, 0.5, 1),
            halign='center'
        )
        support_label.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        layout.add_widget(support_label)
        
        self.add_widget(layout)
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos
    
    def _on_key_text(self, instance, value):
        """Автоматическое форматирование ключа"""
        # Убираем все не-буквенно-цифровые символы
        clean = ''.join(c.upper() for c in value if c.isalnum())
        
        # Ограничиваем длину
        clean = clean[:16]
        
        # Добавляем дефисы каждые 4 символа
        formatted = '-'.join(clean[i:i+4] for i in range(0, len(clean), 4))
        
        # Обновляем текст если он изменился
        if value != formatted:
            instance.text = formatted
    
    def _activate(self, instance):
        """Обработка активации"""
        activation_key = self.key_input.text.strip()
        
        if not activation_key:
            self._show_error("Введите ключ активации")
            return
        
        if len(activation_key.replace('-', '')) < 16:
            self._show_error("Ключ должен содержать 16 символов")
            return
        
        # Блокируем кнопку и показываем загрузку
        self.activate_btn.disabled = True
        self.activate_btn.text = "Активация..."
        self.activate_btn.background_color = (0.3, 0.3, 0.3, 1)
        self.loading_label.text = "Проверка ключа..."
        
        # Запускаем активацию в следующем кадре
        Clock.schedule_once(lambda dt: self._do_activate(activation_key), 0.5)
    
    def _do_activate(self, activation_key):
        """Выполнение активации"""
        try:
            if self.app:
                success, message = self.app.activate_with_key(activation_key)
            else:
                success = False
                message = "Ошибка: приложение не инициализировано"
            
            if success:
                self._show_success(message)
                Clock.schedule_once(lambda dt: self.dispatch('on_activated'), 1.5)
            else:
                self.attempts += 1
                remaining = self.max_attempts - self.attempts
                
                if remaining > 0:
                    self._show_error(f"{message}\nОсталось попыток: {remaining}")
                    self.attempts_label.text = f"Осталось попыток: {remaining}"
                    self.attempts_label.color = (1, 0.5, 0, 1)  # Оранжевый
                else:
                    self._show_error(f"{message}\nПопытки исчерпаны. Обратитесь в поддержку.")
                    self.attempts_label.text = "Попытки исчерпаны"
                    self.attempts_label.color = (1, 0.3, 0.3, 1)  # Красный
                    self.key_input.disabled = True
                    self.activate_btn.disabled = True
                    self.activate_btn.text = "Заблокировано"
                    self.activate_btn.background_color = (0.5, 0.1, 0.1, 1)
                
        except Exception as e:
            self._show_error(f"Ошибка активации: {str(e)}")
        finally:
            # Восстанавливаем кнопку если есть попытки
            if self.attempts < self.max_attempts:
                self.activate_btn.disabled = False
                self.activate_btn.text = "Активировать"
                self.activate_btn.background_color = (0.3, 0.6, 0.3, 1)
                self.loading_label.text = ""
    
    def _show_error(self, message: str):
        """Показ ошибки"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        error_label = Label(
            text="❌ " + message,
            color=(1, 0.3, 0.3, 1),
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        error_label.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        content.add_widget(error_label)
        
        close_btn = Button(
            text="OK",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.5, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title="Ошибка активации",
            content=content,
            size_hint=(0.8, 0.3),
            auto_dismiss=False,
            background_color=(0.2, 0.05, 0.05, 1)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def _show_success(self, message: str):
        """Показ успеха"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        success_label = Label(
            text="✅ " + message,
            color=(0.3, 1, 0.3, 1),
            font_size=sp(18),
            halign='center',
            valign='middle'
        )
        success_label.bind(size=lambda inst, s: setattr(inst, 'text_size', s))
        content.add_widget(success_label)
        
        popup = Popup(
            title="Активация успешна",
            content=content,
            size_hint=(0.8, 0.25),
            auto_dismiss=True,
            background_color=(0.05, 0.2, 0.05, 1)
        )
        popup.open()
    
    def on_activated(self):
        """Событие успешной активации"""
        pass
