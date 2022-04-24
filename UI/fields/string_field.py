# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'string_field.kv')
Builder.load_file(path_to_kv_file)


class StringField(MDTextField):
	def __init__(self, title: str):
		self.title = title.title()
		self.info_text = LANG.get(self.title, '')

		super().__init__()