# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

import db_models
from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'many_to_many_field.kv')


class ManyToManyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title.title()
		self.icon = Settings.ICONS.get(self.title, '')

		super().__init__()

		self.widgets_list = []
		self.fill_content()

	def fill_content(self) -> None:
		pass