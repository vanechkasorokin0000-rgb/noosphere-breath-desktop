"""
Система защиты с офлайн- и онлайн-проверкой.
"""

import hashlib
import os
import json
import logging

logger = logging.getLogger('NoosphereBreath.Protection')


class HardwareFingerprint:
    @staticmethod
    def get_device_fingerprint() -> str:
        try:
            from uuid import getnode
            mac = ':'.join(('%012X' % getnode())[i:i+2] for i in range(0, 12, 2))
            return hashlib.sha256(f"mac:{mac}".encode()).hexdigest()
        except:
            return hashlib.sha256(os.urandom(32)).hexdigest()


class LicenseManager:
    def __init__(self, app_secret: str = ""):
        self.license_dir = self._get_license_dir()
        self.license_file = os.path.join(self.license_dir, '.license.dat')
    
    def _get_license_dir(self) -> str:
        try:
            from kivy.app import App
            return App.get_running_app().user_data_dir
        except:
            return os.path.expanduser('~/.noosphere_breath')
    
    def generate_license(self, user_id: str, key: str) -> dict:
        fp = HardwareFingerprint.get_device_fingerprint()
        return {
            'user_id': user_id,
            'device_fingerprint': fp,
            'activation_key_hash': hashlib.sha256(key.encode()).hexdigest(),
        }
    
    def save_license(self, data: dict) -> bool:
        try:
            os.makedirs(self.license_dir, exist_ok=True)
            with open(self.license_file, 'w') as f:
                json.dump(data, f)
            return True
        except:
            return False
    
    def load_license(self) -> dict:
        if not os.path.exists(self.license_file):
            return None
        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def verify_license(self, data: dict) -> bool:
        if not data:
            return False
        return HardwareFingerprint.get_device_fingerprint() == data.get('device_fingerprint', '')
    
    def is_activated(self) -> bool:
        return self.verify_license(self.load_license())


class ActivationValidator:
    def __init__(self, app_secret: str = "", uid: str = "", app_key: str = "", expected_key_hash: str = ""):
        self.uid = uid
        self.app_key = app_key
        self.expected_key_hash = expected_key_hash
    
    def validate_activation_key(self, key: str) -> bool:
        # Если есть ожидаемый хеш — проверяем по нему
        if self.expected_key_hash:
            key_hash = hashlib.sha256(key.replace('-', '').encode()).hexdigest()
            return key_hash == self.expected_key_hash
        # Иначе — проверяем по uid + app_key
        if self.uid and self.app_key:
            expected = hashlib.sha256(f"{self.uid}_activation_{self.app_key}".encode()).hexdigest()[:16]
            return hashlib.sha256(key.encode()).hexdigest()[:16] == expected
        # Заглушка
        return len(key) >= 16


class AppProtection:
    def __init__(self, app_secret: str = "", embedded_user_id: str = "", embedded_app_key: str = "", expected_key_hash: str = ""):
        self.license_manager = LicenseManager(app_secret)
        self.validator = ActivationValidator(app_secret, embedded_user_id, embedded_app_key, expected_key_hash)
        self.attempts = 0
        self.max_attempts = 3
    
    def activate(self, key: str) -> tuple:
        if self.license_manager.is_activated():
            return True, "Уже активировано"
        
        # Локальная проверка ключа
        if not self.validator.validate_activation_key(key):
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            return False, f"Неверный ключ. Осталось попыток: {remaining}"
        
        # Онлайн-проверка (если есть интернет)
        try:
            from .bot_client import BotClient
            fp = HardwareFingerprint.get_device_fingerprint()
            bot = BotClient()
            success, message = bot.activate_key(key.replace('-', ''), fp, self.validator.uid)
            if not success:
                return False, f"Ошибка сервера: {message}"
        except ImportError:
            # Бот не настроен — разрешаем офлайн-активацию
            pass
        except Exception as e:
            # Нет интернета — разрешаем офлайн-активацию
            logger.warning(f"Офлайн-активация (нет связи): {e}")
        
        # Сохраняем локальную лицензию
        lic = self.license_manager.generate_license(self.validator.uid, key)
        if self.license_manager.save_license(lic):
            return True, "Активация успешна!"
        return False, "Ошибка сохранения лицензии"
    
    def is_activated(self) -> bool:
        return self.license_manager.is_activated()
