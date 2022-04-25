# -*- coding: utf-8 -*-

import os
import re

from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'phone_field.kv')
Builder.load_file(path_to_kv_file)


_PHONE_NUMBER_PATTERN = r'\+?[78](\d{3})(\d{3})(\d{2})(\d{2})'
_REPL = r'+7 (\1) \2-\3-\4'


class PhoneField(MDTextField):
	def __init__(self, title: str):
		self.title = title.title()
		self.info_text = LANG.get(self.title, '')

		super().__init__()

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		super().insert_text(substring, from_undo)

		update_text = self.numbers_to_phone(self.text)
		self.text = update_text

	@staticmethod
	def numbers_to_phone(numbers: str) -> str:
		only_numbers = ''.join(re.findall(r'\d', numbers))
		if len(only_numbers) == 11:
			result = re.sub(_PHONE_NUMBER_PATTERN, _REPL, only_numbers)
			return result

		return numbers

	def get_value(self) -> str:
		return self.numbers_to_phone(self.text)