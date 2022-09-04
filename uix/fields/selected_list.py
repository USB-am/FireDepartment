import os
from typing import Union

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_KV_DIR, LOCALIZED
from data_base import db
from uix.dialog import FDDialog


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'selected_list.kv')
Builder.load_file(path_to_kv_file)


class SelectedListElement(MDBoxLayout):
	''' Элемент спика SelectedList '''

	def __init__(self, db_entry: db.Model, group: str=None):
		self.db_entry = db_entry
		self.group = group
		self.dialog = FDDialog(self.db_entry.title, MDBoxLayout())

		super().__init__()

		self.setup()

	def setup(self) -> None:
		self.ids.button.bind(on_release=lambda e: self.dialog.open())

	@property
	def active(self) -> bool:
		return self.ids.checkbox.active

	def activate(self) -> None:
		self.ids.checkbox.active = True

	def deactivate(self) -> None:
		self.ids.checkbox.active = False


class SelectedList(MDBoxLayout):
	''' Список с возможностью выбора элементов '''

	def __init__(self, icon: str, title: str, values: list, group: str=None,
	             **options):
		self.icon = icon
		self.title = title
		self.values = values
		self.group = group

		self.display_text = LOCALIZED.translate(title)

		super().__init__(**options)

		self.fill_content(values)

	def fill_content(self, values: list) -> None:
		container = self.ids.elements

		for value in values:
			element = SelectedListElement(value, self.group)
			container.add_widget(element)

	def binding(self, path_manager) -> None:
		create_screen_name = f'create_{self.title}'.lower()
		self.ids.redirect_button.bind(
			on_release=lambda e: path_manager.forward(create_screen_name))

	def get_value(self) -> list:
		elements = self.ids.elements.children
		output = [element.db_entry for element in elements if element.active]

		return output

	def set_value(self, value: Union[list, int]) -> None:
		print(f'SelectedList.set_value({value}) is started')
		elements = self.ids.elements.children
		[element.deactivate() for element in elements]

		if isinstance(value, list):
			value_ids = list(map(lambda val: val.id, value))

			for element in elements:
				if element.db_entry.id in value_ids:
					element.activate()

		if isinstance(value, int):
			[element.activate() for element in elements \
			                    if element.db_entry.id == value]