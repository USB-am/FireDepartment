# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from app.tools.custom_widgets import FDTextField
from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'string_field.kv')
Builder.load_file(path_to_kv_file)


class StringField(FDTextField):
	icon = 'form-textbox'

	def __init__(self, title: str):
		self.title = title

		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()