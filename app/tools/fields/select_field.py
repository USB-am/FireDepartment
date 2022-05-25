# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.app import MDApp
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

		self._update_items_color()

		self.value = None

	def open(self) -> None:
		super().open()

		self._update_items_color()

	def _item_creation(self) -> list:
		items = []
		theme = ColorTheme.query.first()

		for text in self.data:
			theme_key = theme.primary_palette\
				if not self.title in ('primary_palette', 'accent_palette') else text
			hue_key = theme.primary_hue if self.title != 'primary_hue' else text

			items.append({
				'viewclass': 'OneLineListItem',
				'text': text,
				'bg_color': COLORS[theme_key][hue_key],
				'on_release': lambda x=text: self._update_value(x)
			})

		return items

	def _update_value(self, item: str) -> None:
		self.value = item

	def _update_items_color(self) -> None:
		theme = MDApp.get_running_app().theme_cls

		if self.title in ('primary_palette', 'accent_palette'):
			for item in self.items:
				item['bg_color'] = COLORS[item['text']][theme.primary_hue]


class SelectField(MDBoxLayout):
	icons = {
		'primary_palette': 'shape',
		'accent_palette': 'exclamation-thick',
		'primary_hue': 'format-size'
	}

	def __init__(self, title: str, update_theme_method):
		self.title = title
		self.update_theme_method = update_theme_method
		self.translate_text = LOCALIZED.translate(self.title)
		self.display_text = self.translate_text[:]
		self.icon = self.icons.get(title, 'bus')

		super().__init__()

		self.menu = DropdownMenu(
			caller=self.ids.open_dropmenu_button,
			title=self.title,
			data=self._get_data()
		)
		self.menu.bind(on_dismiss=lambda x: self._change_theme())

	def _change_theme(self) -> None:
		self.update_theme_method({self.title: self.get_value()})
		self._update_label()

	def _update_label(self):
		self.ids.label.text = f'{self.translate_text} ({self.menu.value})'

	def _get_data(self) -> list:
		if self.title in ('primary_palette', 'accent_palette'):
			return tuple(COLORS.keys())[:-2]
		elif self.title in ('primary_hue',):
			return COLORS['Red'].keys()
		else:
			return []

	def get_value(self) -> str:
		return self.menu.value

	def set_value(self, value: str) -> None:
		self.menu.value = value
		self._update_label()