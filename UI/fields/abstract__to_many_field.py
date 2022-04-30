# -*- coding: utf-8 -*-

from sqlalchemy.orm.collections import InstrumentedList
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

import db_models
from settings import settings as Settings
from settings import LANG
from ._to_many_field import CheckboxItem


class _ToManyField(MDBoxLayout):
	def __init__(self, title: str, group: bool=False):
		self.title = title.title()
		self.icon = Settings.ICONS.get(self.title, '')
		self.title_label_text = LANG.get(self.title)
		if group:
			self.group = self.title
		else:
			self.group = group

		super().__init__()

		self.widgets_list = []
		self.fill_content()

	def fill_content(self) -> None:
		content = self.ids.container
		content.clear_widgets()

		db_table = getattr(db_models, self.title.replace('_', ''))
		db_rows = db_table.query.all()

		for db_row in db_rows:
			if self.group:
				checkbox_item = CheckboxItem(db_row, group=self.group)
			else:
				checkbox_item = CheckboxItem(db_row)

			self.widgets_list.append(checkbox_item)
			content.add_widget(checkbox_item)

		if len(self.widgets_list) == 0:
			content.add_widget(MDLabel(
				text='[Пусто]',
				size_hint=(1, None),
				size=(self.width, 50),
				text_size=self.size,
				halign='center'
			))


class ForeignKeyField(_ToManyField):
	def __init__(self, title: str):
		self.column_name = title
		super().__init__(title, True)

	def get_value(self) -> int:
		for widget in self.widgets_list:
			if widget.is_active():
				return widget.db_row.id


class ManyToManyField(_ToManyField):
	def __init__(self, title: str):
		self.column_name = title
		title = title[:-1]
		super().__init__(title, False)

	def get_value(self) -> list:
		result = InstrumentedList()

		for widget in self.widgets_list:
			if widget.is_active():
				result.append(widget.db_row)

		return result