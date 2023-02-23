from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config import paths
from data_base import db


Builder.load_file(paths.SELECTED_LIST_FIELD)


class _SelectListItem(MDBoxLayout):
	''' Элемент списка FDSelectList '''

	def __init__(self, db_entry: db.Model, group: str=None):
		self.db_entry = db_entry
		self.group = group

		super().__init__()

	@property
	def checkbox(self) -> bool:
		return self.ids.checkbox.active

	@checkbox.setter
	def checkbox(self, value: bool) -> None:
		self.ids.checkbox.active = value


class FDSelectList(MDBoxLayout):
	''' Список с checkbox'ами '''

	icon = StringProperty()
	title = StringProperty()
	group = StringProperty(None)

	def add(self, row_data: db.Model) -> None:
		element = _SelectListItem(row_data, group=self.group)
		self.ids.lst.add_widget(element)

	def get_value(self) -> list:
		container = self.ids.lst
		values = [child.db_entry for child in container.children \
			if child.checkbox]

		return values

	def set_value(self, values: list) -> None:
		container = self.ids.lst

		for child in container.children:
			child.checkbox = False

			if child.db_entry in values:
				child.checkbox = True