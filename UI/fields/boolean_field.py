# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'boolean_field.kv')
Builder.load_file(path_to_kv_file)


class BooleanField(MDBoxLayout):
	def __init__(self, title: str):
		self.column_name = title
		self.title = title.title()
		self.info_text = LANG.get(self.title, self.title)

		super().__init__()

	def get_value(self) -> bool:
		return self.ids.switch.active