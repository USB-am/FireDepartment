# -*- coding: utf-8 -*-

from kivymd.uix.boxlayout import MDBoxLayout

import db_models
from settings import settings as Settings
from ._to_many_field import CheckboxItem


class ForeignKeyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title.title()
		self.icon = Settings.ICONS.get(self.title, '')

		super().__init__()

		self.widgets_list = []
		self.fill_content()

	def fill_content(self) -> None:
		content = self.ids.foreign_key_container
		content.clear_widgets()

		db_table = getattr(db_models, self.title)
		db_rows = db_table.query.all()

		for db_row in db_rows:
			checkbox_item = CheckboxItem(db_row, group=self.title)
			self.widgets_list.append(checkbox_item)
			content.add_widget(checkbox_item)

	def get_value(self) -> int:
		for widget in self.widgets_list:
			if widget.is_active():
				return widget.db_row.id