# -*- coding: utf-8 -*-

import os
from datetime import datetime

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'work_graph.kv')
Builder.load_file(path_to_kv_file)


_GRAPH_TYPES = ('-', 'Всегда', '1/3', '5/2')


class CustomDatePicker(MDDatePicker):
	pass


class CustomDropDown(MDDropdownMenu):
	pass


class IconListItem(OneLineIconListItem):
	icon = StringProperty()


class WorkGraph(MDBoxLayout):
	DATE_PICKER = None
	DROP_DOWN = None

	def __init__(self, title: str):
		self.column_name = title
		self.title = title.title()
		self.title_label_text = LANG.get(self.title, '')
		self.items = [str(i+1) for i in range(50)]

		self.date_ = None
		self.graph = None

		super().__init__()

		self.create_dropdown()

	def __str__(self) -> str:
		return f'{self.date_} -> {self.graph}'

	def open_date_picker(self) -> None:
		if self.DATE_PICKER is None:
			self.DATE_PICKER = CustomDatePicker()

		self.DATE_PICKER.bind(on_save=self.save_date)
		self.DATE_PICKER.open()

	def save_date(self, instance: CustomDatePicker, date: datetime.date,\
		date_range: list) -> None:

		self.date_ = date

	def create_dropdown(self) -> None:
		if self.DROP_DOWN is None:
			menu_items = [
				{
					'viewclass': 'IconListItem',
					'icon': Settings.ICONS.get(self.title, ''),
					'text': graph_type,
					'height': 50,
					'on_release': lambda x=graph_type: self.set_item(x),
				} for graph_type in _GRAPH_TYPES
			]
			self.DROP_DOWN = CustomDropDown(
				caller=self.ids.dropdown_item,
				items=menu_items,
				position='center',
				width_mult=4
			)
			self.DROP_DOWN.bind()

	def set_item(self, text_item):
		self.ids.dropdown_item.set_item(text_item)
		self.DROP_DOWN.dismiss()

	def get_value(self) -> dict:
		return {
			'work_day': None,
			'work_type': None
		}