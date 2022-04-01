# -*- coding: utf-8 -*-

from os.path import join as os_join

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.button import Button

import config as Config
from UI.custom_screen import CustomScreen
from UI.custom_widgets import FDTitleLabel, FDButton, FDSeparator, FDColorInput
import db_models


path_to_kv_file = os_join(Config.PATTERNS_DIR, 'settings.kv')
Builder.load_file(path_to_kv_file)

DB_TABLES = [db_models.Tag, db_models.Rank, db_models.Position, \
	db_models.Person, db_models.Post
]


class TableSettings(BoxLayout):
	def __init__(self, table):
		self.table = table
		self.view_text = self.table.__tablename__
		self.to_create_page = f'create_{self.table.__tablename__.lower()}'
		self.to_list_edit = f'edit_{self.table.__tablename__.lower()}s'

		super().__init__()


class CustomColorInput(FDButton):
	def __init__(self, title: str):
		self.title = title
		self.color_input = FDColorInput(self.title)

		super().__init__()

		self.bind(on_press=self.color_input.open)

	def get_value(self) -> tuple:
		print('CustomColorInput get value')
		return self.color_input.get_value()


class CustomizationSettings(BoxLayout):
	def __init__(self):
		super().__init__()

		self.fill_custom_inputs()

	def fill_custom_inputs(self) -> None:
		self.add_widget(CustomColorInput('Text #1'))
		self.add_widget(CustomColorInput('Text #2'))
		self.add_widget(CustomColorInput('Text #3'))


class ToCustomSettingsButton(Button):
	pass


class Settings(CustomScreen):
	name = 'settings'

	def __init__(self):
		super().__init__()

		self.__data_base_settings()
		self.ids.settings_list.add_widget(FDSeparator())
		# self.__customization_settings()
		self.ids.settings_list.add_widget(ToCustomSettingsButton())

	def __data_base_settings(self) -> None:
		container = self.ids.settings_list

		container.add_widget(FDTitleLabel(
			text='Изменение базы данных:',
			size_hint=(1, None),
			size=(self.width, 30)
		))

		for table in DB_TABLES:
			widget = TableSettings(table)
			container.add_widget(widget)

	def __customization_settings(self) -> None:
		container = self.ids.settings_list

		container.add_widget(FDTitleLabel(
			text='Внешний вид:',
			size_hint=(1, None),
			size=(self.width, 30)
		))

		container.add_widget(CustomizationSettings())