# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from app.tools.custom_widgets import FDTextField
from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'integer_field.kv')
Builder.load_file(path_to_kv_file)


class IntegerField(FDTextField):
	icon = 'numeric'

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		if substring.isdigit():
			super().insert_text(substring, from_undo)