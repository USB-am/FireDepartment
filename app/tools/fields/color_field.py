# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDThemePicker

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets import FDColorPicker


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'color_field.kv')
Builder.load_file(path_to_kv_file)


class ColorField(MDBoxLayout):
	icon = 'palette'

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

		self.theme_picker = MDThemePicker()
		self.theme_picker.bind(on_pre_dismiss=lambda e: print('on_pre_dismiss'))
		self._color_picker = FDColorPicker(title=self.display_text)

	def open_dialog(self) -> None:
		# self._color_picker.open()
		self.theme_picker.open()

	def get_value(self) -> list:
		return self._color_picker.current_color

	def set_value(self, color: list) -> None:
		self._color_picker.current_color = color