# -*- coding: utf-8 -*-

from kivymd.uix.boxlayout import MDBoxLayout

import db_models
from settings import settings as Settings
from ._to_many_field import CheckboxItem


class _ToManyField(MDBoxLayout):
	def __init__(self, title: str, group: bool=False):
		self.title = title.title()
		self.icon = Settings.ICONS.get(self.title, '')
		self.group = group

		super().__init__()

		self.widgets_list = []
		self.fill_content()

	def fill_content(self) -> None:
		content = self.ids.container
		content.clear_widgets()

		db_table = getattr(db_models, self.title)
		db_rows = db_table.query.all()

		for db_row in db_rows:
			if self.group:
				checkbox_item = CheckboxItem(db_row, group=self.group)
			else:
				checkbox_item = CheckboxItem(db_row)

			self.widgets_list.append(checkbox_item)
			content.add_widget(checkbox_item)


class ForeignKeyField(_ToManyField):
	def __init__(self, title: str):
		super().__init__(title, True)

	def get_value(self) -> int:
		for widget in self.widgets_list:
			if widget.is_active():
				return widget.db_row.id


class ManyToManyField(_ToManyField):
	def __init__(self, title: str):
		super().__init__(title, False)

	def get_value(self) -> list:
		result = []

		for widget in self.widgets_list:
			if widget.is_active():
				result.append(widget.db_row.id)

		return result