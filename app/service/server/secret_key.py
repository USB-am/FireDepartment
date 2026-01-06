import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

from config import SECRET_KEY_PATH
from service.singleton import _Singleton


class _SecretKeyManager:
    def __init__(self):
        self.config_path = Path(SECRET_KEY_PATH)
        self._last_modified = 0
        self._cache = None
        self._cache_hash = None

    def _load_secrets(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}

        current_modified = self.config_path.stat().st_mtime

        if current_modified > self._last_modified \
            or self._cache is None:

            with open(self.config_path, 'r') as f:
                self._cache = json.load(f)
                self._last_modified = current_modified
                content = json.dumps(self._cache, sort_keys=True)
                self._cache_hash = hashlib.sha256(content.encode()).hexdigest()

        return self._cache

    def get_secret(self) -> Optional[str]:
        secrets = self._load_secrets()
        return secrets.get('secret_key')

    def update_secret(self, new_value: str) -> None:
        secrets = self._load_secrets()
        secrets['secret_key'] = new_value

        with open(self.config_path, 'w') as f:
            json.dump(secrets, f, indent=2)

        self._last_modified = 0


class SecretKey(metaclass=_Singleton):
    def __init__(self):
        self._manager = _SecretKeyManager()

    @property
    def value(self) -> Optional[str]:
        return self._manager.get_secret()

    @value.setter
    def value(self, new_secret_key: str) -> None:
        if not isinstance(new_secret_key, str):
            raise AttributeError(f'The attribute is an [{type(new_secret_key)}] type and a str is expected.')
        self._manager.update_secret(new_secret_key)
