# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets import CustomScreen, FDDialog
from app.tools.custom_widgets.label import FDLabel
from app.tools import fields


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_db_screens.kv')
Builder.load_file(path_to_kv_file)


class AbstractUpdateDBScreen(CustomScreen):
	''' Abstract class to Create and Update screens '''

	def __init__(self):
		super().__init__()

		self.bind(on_pre_enter=self.update_to_many_fields)

		self.fields = {}

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

	def update_to_many_fields(self, instance: CustomScreen) -> None:
		''' Update ForeignKeyFields and ManyToManyFields to pre load screen '''
		for field in self.fields.values():
			if isinstance(field, (fields.ManyToManyField, fields.ForeignKeyField)):
				field.update_content()

	def clear_fields_content(self) -> None:
		''' Clears all fields from the entered data '''
		[field.clear() for field in self.fields.values()]

	def get_values(self) -> dict:
		''' Returns field values '''
		return {title: field.get_value() for title, field in self.fields.items()}