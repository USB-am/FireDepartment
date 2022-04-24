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


class PhoneField(MDTextField):
	def __init__(self, title: str):
		self.title = title.title()
		self.info_text = LANG.get(self.title, '')
		# print(Settings.FONT_COLOR)

		super().__init__()

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		super().insert_text(substring, from_undo)
		# print(self.text)
		numbers = ''.join(re.findall(r'\d', self.text))
		if len(numbers) == 11:
			self.text = self.numbers_to_phone(numbers)
		print(self.text)

	@staticmethod
	def numbers_to_phone(numbers) -> str:
		return '8 (800) 555 35 35'