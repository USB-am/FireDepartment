# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'fields', 'string_field.kv')
Builder.load_file(path_to_kv_file)


class StringField(MDTextField):
	def __init__(self, title: str):
		title = title.title()
		self.title = LANG.get(title, title)
		# self.db_row = db_row

		super().__init__()