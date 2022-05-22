# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'select_field.kv')
Builder.load_file(path_to_kv_file)


class SelectField(MDBoxLayout):
	icons = {}

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self.icon = self.icons.get(title, 'bus')

		super().__init__()

	def get_value(self) -> str:
		pass

	def set_value(self, value: str) -> None:
		pass