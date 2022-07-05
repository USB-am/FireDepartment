# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR, LOCALIZED
from .abstract_to_many_field import ElementToManyField
import data_base


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields',
	'emergency_display_field.kv')
Builder.load_file(path_to_kv_file)


class DisplayElementToManyField(ElementToManyField):
	def __init__(self, element: data_base.db, group: str=None):
		super().__init__(element, group)
		self.display_text = '{name}\n{phone}'.format(
			name=element.title,
			phone=element.phone_1)
		self.ids.btn.text = self.display_text


class ToManyDisplayField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)

		super().__init__()

	def update(self, values: list) -> None:
		content = self.ids.content
		content.clear_widgets()

		for value in values:
			content.add_widget(DisplayElementToManyField(value))