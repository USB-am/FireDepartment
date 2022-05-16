# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'boolean_field.kv')
Builder.load_file(path_to_kv_file)


class BooleanField(MDBoxLayout):
	icon = 'truck-fast'

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

	def get_value(self) -> bool:
		return self.ids.switch.active

	def clear(self) -> None:
		self.ids.switch.active = False