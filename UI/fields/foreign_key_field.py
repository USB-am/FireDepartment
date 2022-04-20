# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

import db_models
from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'fields', 'foreign_key_field.kv')
Builder.load_file(path_to_kv_file)


class ManyTo_Item(MDBoxLayout):
	def __init__(self, item_info):
		print(type(item_info))

		self.item_info = item_info

		super().__init__()


class ForeignKeyField(MDBoxLayout):
	def __init__(self, title: str):
		title = title.title()

		self.group_name = title
		self.table = getattr(db_models, title)
		self.title = LANG.get(title, title)

		super().__init__()

		self.fill_container()

	def fill_container(self) -> None:
		container = self.ids.container
		container.clear_widgets()

		items = self.table.query.all()

		for item in items:
			container.add_widget(ManyTo_Item(
				item_info=item
			))