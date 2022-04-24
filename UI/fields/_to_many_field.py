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

class TableInfoContent(MDBoxLayout):
	def __init__(self, db_row: db_models.db.Model):
		self.db_row = db_row

		super().__init__()

		self.fill_list()

	def fill_list(self) -> None:
		container = self.ids.table_info_list
		container.clear_widgets()

		fields_names = self.db_row.get_fields().keys()

		for field in fields_names:
			info = getattr(self.db_row, field)
			field_name = LANG.get(field.title(), '')
			container.add_widget(MDLabel(
				size_hint=(1, None),
				size=(self.width, 50),
				text=f'{field_name}: {info}'
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