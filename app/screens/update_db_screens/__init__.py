# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets import CustomScreen
from app.tools import fields


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_db_screens.kv')
Builder.load_file(path_to_kv_file)


class AbstractUpdateDBScreen(CustomScreen):
	''' Abstract class to Create and Update screens '''

	def __init__(self):
		super().__init__()

		self.fields = {}

		self.update_title()
		self.update_content()

	def update_title(self) -> None:
		''' Set toolbar title '''
		translate_text = LOCALIZED.translate(self.name)
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		''' Create fields '''
		content = self.ids.content
		content.clear_widgets()

		for title, field_name in self.table.get_fields().items():
			try:
				field = getattr(fields, field_name)(title)
				content.add_widget(field)
				self.fields[title] = field
			except Exception as error:
				print('[{}] {}'.format(
					error.__class__.__name__,
					str(error)
				))

	def get_values(self) -> dict:
		''' Returns field values '''
		return {title: field.get_value() for title, field in self.fields.items()}