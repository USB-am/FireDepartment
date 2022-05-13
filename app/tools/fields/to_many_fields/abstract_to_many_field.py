# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR, LOCALIZED
import data_base


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'to_many_fields',
	'abstract_to_many_field.kv')
Builder.load_file(path_to_kv_file)


class ElementToManyField(MDBoxLayout):
	def __init__(self, element: data_base.db, group: str=None):
		self._element = element
		# self.icon = self._element.icon
		self.display_text = self._element.title
		self.group = group

		super().__init__()


class AbstractToManyField(MDBoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self._table = getattr(data_base, self._table_name)
		self.icon = self._table.icon
		self.to_create_screen = f'create_{self._table_name.lower()}'

		super().__init__()

		self.fill_content()

	def fill_content(self) -> None:
		elements = self._table.query.all()

		if not elements:
			return

		container = self.ids.content
		container.clear_widgets()

		for element in elements:
			container.add_widget(ElementToManyField(
				element=element,
				group=self.group
			))