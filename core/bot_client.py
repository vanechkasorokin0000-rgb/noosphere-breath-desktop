"""Клиент для связи с сервером активации."""

import hashlib
import logging
from typing import Tuple

logger = logging.getLogger('NoosphereBreath.BotClient')

ACTIVATION_SERVER = "http://noosphereproject.ru:5000"


class BotClient:
    def __init__(self):
        self.server_url = ACTIVATION_SERVER
    
    def activate_key(self, activation_key: str, device_fingerprint: str, user_id: str = "") -> Tuple[bool, str]:
        try:
            import requests
            
            key_hash = hashlib.sha256(activation_key.encode()).hexdigest()
            
            response = requests.post(
                f"{self.server_url}/activate",
                json={
                    "key_hash": key_hash,
                    "device_id": device_fingerprint,
                    "user_id": user_id
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    return data.get("activated", False), data.get("message", "")
            
            return False, "Ошибка сервера"
            
        except ImportError:
            logger.warning("requests не установлен")
            return True, "Офлайн-режим"
        except Exception as e:
            logger.error(f"Ошибка: {e}")
            return True, "Офлайн-режим (нет связи)"
