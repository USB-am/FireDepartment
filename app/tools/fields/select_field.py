# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
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

		self.value = None

	def _item_creation(self) -> list:
		items = []
		theme = ColorTheme.query.first()

		for text in self.data:
			# TODO: сейчас выбор только из theme.theme. Сделать еще из theme.accent
			theme_key = theme.theme\
				if not self.title in ('theme', 'accent') else text
			hue_key = theme.hue if self.title != 'hue' else text
			items.append({
				'viewclass': 'OneLineListItem',
				'text': text,
				'bg_color': COLORS[theme_key][hue_key],
				'on_release': lambda x=text: self._update_value(x)
			})

		return items

	def _update_value(self, item: str) -> None:
		self.value = item
		self.dismiss()


class SelectField(MDBoxLayout):
	icons = {
		'theme': 'shape',
		'accent': 'exclamation-thick',
		'hue': 'format-size'
	}

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self.icon = self.icons.get(title, 'bus')

		super().__init__()

		self.menu = DropdownMenu(
			caller=self.ids.open_dropmenu_button,
			title=self.title,
			data=self._get_data()
		)

	def _get_data(self) -> list:
		if self.title in ('theme', 'accent'):
			return tuple(COLORS.keys())[:-2]
		elif self.title in ('hue',):
			return COLORS['Red'].keys()
		else:
			return []

	def get_value(self) -> str:
		return self.menu.value