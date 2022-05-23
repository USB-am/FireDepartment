# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu

from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'select_field.kv')
Builder.load_file(path_to_kv_file)


class SelectField(MDBoxLayout):
	icons = {
		'theme': 'shape',
		'accent': 'exclamation-thick',
		'hue': 'format-size',
		'style': 'theme-light-dark'
	}

	def __init__(self, title: str, data: list):
		self.title = title
		self.data = data
		self.display_text = LOCALIZED.translate(self.title)
		self.icon = self.icons.get(title, 'bus')

		super().__init__()

		menu_items = [{
			'icon': self.icon,
			'viewclass': 'OneLineListItem',
			'text': text
		} for text in self.data]
		self.menu = MDDropdownMenu(
			caller=self.ids.open_dropmenu_button,
			items=menu_items,
			width_mult=3,
			max_height=224
		)

	def get_value(self) -> str:
		pass

	def set_value(self, value: str) -> None:
		pass