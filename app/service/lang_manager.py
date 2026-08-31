import os
import json

from kivy.event import EventDispatcher
from kivy.properties import DictProperty, StringProperty


class LangManager(EventDispatcher):
    data: dict[str, str] = DictProperty({})
    current_lang: str = StringProperty('en')

    def __init__(self, default_lang='en', locales_dir='locales', **kwargs):
        super().__init__(**kwargs)
        self.locales_dir = locales_dir
        self.switch_lang(default_lang)

    def switch_lang(self, lang_code: str) -> None:
        file_path = os.path.join(self.locales_dir, f'{lang_code}.json')
        
        if os.path.exists(file_path):
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    self.data = json.load(f)
                    self.current_lang = lang_code
            except Exception as e:
                print(f'Ошибка загрузки файла локализации {file_path}: {e}')
        else:
            print(f'Файл локализации не найден: {file_path}')

    def get_text(self, key: str, default: str='') -> str:
        return self.data.get(key, default if default else key)
