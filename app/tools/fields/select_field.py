# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.theming import ThemeManager

from config import PATTERNS_DIR, LOCALIZED
from data_base import ColorTheme


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'select_field.kv')
Builder.load_file(path_to_kv_file)


COLORS = ThemeManager().colors


class DropdownMenu(MDDropdownMenu):
	def __init__(self, caller, title: str, data: list):
		self.caller = caller
		self.data = data
		self.title = title

		self.width_mult = 3	# Menu width
		self.max_height = 224	# Menu height (56 - 1 item)
		self.items = self._item_creation()

		super().__init__()

	def _item_creation(self) -> list:
		items = []
		theme = ColorTheme.query.first()

		for text in self.data:
			theme_key = theme.theme if not self.title in ('theme', 'accent') else text
			hue_key = theme.hue if self.title != 'hue' else text
			items.append({
				'viewclass': 'MenuItem',
				'text': text,
				'bg_color': COLORS[theme_key][hue_key],
				'on_release': lambda x=text: print(f'You selected {x} item')
			})

		return items


class MenuItem(OneLineListItem):
	pass


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

		self.menu = DropdownMenu(
			caller=self.ids.open_dropmenu_button,
			title=self.title,
			data=self.data
		)

	def get_value(self) -> str:
		theme = ColorTheme.query.first()
		print(f'theme = {theme}')

	def set_value(self, value: str) -> None:
		pass