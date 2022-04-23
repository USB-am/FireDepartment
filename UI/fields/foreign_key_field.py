# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

import db_models
from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'foreign_key_field.kv')
Builder.load_file(path_to_kv_file)


class CheckboxItem(MDBoxLayout):
	def __init__(self, db_row: db_models.db.Model):
		self.db_row = db_row

		super().__init__()


class ForeignKeyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title.title()
		self.icon = Settings.ICONS.get(self.title, '')

		super().__init__()

		self.fill_content()

	def fill_content(self) -> None:
		content = self.ids.foreign_key_container
		content.clear_widgets()

		db_table = getattr(db_models, self.title)
		db_rows = db_table.query.all()

		for db_row in db_rows:
			content.add_widget(CheckboxItem(db_row))