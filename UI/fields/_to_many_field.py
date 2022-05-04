# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel

import db_models
from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'abstract__to_many_field.kv')
Builder.load_file(path_to_kv_file)


def get_localized_text(text: str) -> str:
	return LANG.get(text, text)


def default_text_examination(method):
	def wrapper(column: str, value: str):
		localized_column_name = get_localized_text(column)

		if value is None:
			return f'{localized_column_name}: [Пусто]'

		return method(localized_column_name, value)

	return wrapper


class FieldsText(MDLabel):
	@staticmethod
	@default_text_examination
	def stringfield(column: str, value: str) -> str:
		''' Returned "ColumnName: Text" '''
		return f'{column}: {value}'

	@staticmethod
	@default_text_examination
	def phonefield(column: str, value: str) -> str:
		''' Returned "ColumnName: PhoneNumber" '''
		return f'{column}: {value}'

	@staticmethod
	@default_text_examination
	def workdayfield(column: str, value: str) -> str:
		''' Returned "ColumnName: Date" '''
		return f'{column}: {value}'

	@staticmethod
	# @default_text_examination
	def foreignkeyfield(column: str, value: int) -> str:
		''' Returned "ColumnName: OnceElement" '''
		return f'{column}: {value}'

	@staticmethod
	@default_text_examination
	def manytomanyfield(column: str, value: list) -> str:
		'''
		Returned list.
			ColumnName:
			 - value[0]
			 - value[1]
			 - value[n]
		'''

		return '{column_name}:{values}'.format(
			column_name=column,
			values=''.join([f'\n - {val}' for val in value])
		)


class _TableInfoContent(MDBoxLayout):
	def __init__(self, db_row: db_models.db.Model):
		self.db_row = db_row

		super().__init__()

		self.fill_list()

	def fill_list(self) -> None:
		container = self.ids.table_info_list
		container.clear_widgets()

		table_columns = self.db_row.get_fields()

		for column, field in table_columns.items():
			info = getattr(self.db_row, column)
			field_name = LANG.get(column.title(), '')
			try:
				container.add_widget(MDLabel(
					size_hint=(1, None),
					size=(self.width, 50),
					text=getattr(FieldsText, field.lower())(
						column.title(), info
					)
				))
			except Exception as e:
				print(column, field, e)


class TableInfoContent(MDBoxLayout):
	def __init__(self, db_row: db_models.db.Model):
		self.db_row = db_row

		super().__init__()

		self.fill_list()

	def fill_list(self, clear: bool=False) -> None:
		content = self.ids.table_info_list
		content.clear_widgets()

		table_columns = self.db_row.get_fields()

		for key, value in table_columns.items():
			content.add_widget(MDLabel(
				size_hint=(1, None),
				size=(self.width, 50),
				text=f'{key}: {value}'
			))


class TableInfo(MDDialog):
	def __init__(self, db_row: db_models.db.Model):
		self.title = str(db_row)
		self.content_cls = TableInfoContent(db_row)

		super().__init__(type='custom')


class CheckboxItem(MDBoxLayout):
	def __init__(self, db_row: db_models.db.Model, group: str=None):
		self.db_row = db_row
		self.text = str(self.db_row)
		self.group = group
		self.dialog = None

		super().__init__()

		self.ids.show_info_button.bind(on_press=self.open_dialog)

	def open_dialog(self, instance) -> None:
		if self.dialog is None:
			self.dialog = self._create_dialog()

		self.dialog.open()

	def _create_dialog(self) -> MDDialog:
		dialog = TableInfo(self.db_row)

		return dialog

	def is_active(self) -> bool:
			return self.ids.checkbox.state == 'down'