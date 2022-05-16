# -*- coding: utf-8 -*-

import os
import re

from kivy.lang import Builder

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets import FDTextField


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'phone_field.kv')
Builder.load_file(path_to_kv_file)


class PhoneField(FDTextField):
	icons = {
		'phone_1': 'phone',
		'phone_2': 'phone-plus',
	}

	def __init__(self, title: str):
		self.title = title
		self.icon = self.icons.get(self.title, 'phone')
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		super().insert_text(substring, from_undo)