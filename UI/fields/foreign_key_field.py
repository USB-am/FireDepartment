# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from settings import settings as Settings


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'fields', 'foreign_key_field.kv')
Builder.load_file(path_to_kv_file)


class ForeignKeyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title

		super().__init__()