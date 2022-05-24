# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox

from config import PATTERNS_DIR, LOCALIZED


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'style_radio_field.kv')
Builder.load_file(path_to_kv_file)


class FDCheckbox(MDBoxLayout):
	def __init__(self, title: str, group: str=None):
		self.title = title
		self.group = group
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

		self.checkbox.active = True

	@property
	def checkbox(self) -> MDCheckbox:
		return self.ids.checkbox

	@property
	def active(self) -> bool:
		return self.checkbox.active

	@active.setter
	def active(self, value: bool) -> None:
		self.checkbox.active = value


class RadioContainer(MDBoxLayout):
	def __init__(self, items: tuple, group: str=None):
		super().__init__()

		self.group = group
		self.items = self._creation_radiobuttons(items)

	def _creation_radiobuttons(self, titles: list) -> list:
		result = []

		for item in titles:
			radio_button = FDCheckbox(item, self.group)
			radio_button.checkbox.bind(on_release=self._check_pressed)
			result.append(radio_button)
			self.add_widget(radio_button)

		return result

	def _check_pressed(self, instance: MDCheckbox) -> None:
		if not instance.active:
			instance.active = True

	def get_value(self) -> str:
		return tuple(filter(lambda layout: layout.active, self.items))[0].title

	def set_value(self, value: str) -> None:
		''' Set active state to checkbox '''
		tuple(filter(
			lambda layout: layout.title==value,
			self.items
		))[0].active = True


class StyleRadioField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self.icon = 'theme-light-dark'

		super().__init__()

		self.radio_container = RadioContainer(
			items=('Light', 'Dark'),
			group='theme_style'
		)
		self.add_widget(self.radio_container)

	def get_value(self) -> str:
		self.radio_container.get_value()

	def set_value(self, value: str) -> None:
		self.radio_container.set_value(value)