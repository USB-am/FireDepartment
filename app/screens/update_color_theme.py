# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.card import MDSeparator

from app.tools.custom_widgets import CustomScreen, Submit
from app.tools import fields as FIELDS
from config import PATTERNS_DIR, LOCALIZED
from data_base import db, ColorTheme
from data_base.tools import check_db_commit_except


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_color_theme.kv')
Builder.load_file(path_to_kv_file)


class UpdateColorTheme(CustomScreen):
	name = 'update_color_theme'
	table = ColorTheme

	def __init__(self):
		super().__init__()

		self.widgets = {}

		self.update_title()
		self.update_content()

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate(self.name)
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		current_theme = self.table.query.first()
		table_fields = self.table.get_fields()

		for column_name, field_name in table_fields.items():
			field = getattr(FIELDS, field_name)(column_name, self.update_theme)
			field.set_value(getattr(current_theme, column_name))

			content.add_widget(field)
			content.add_widget(MDSeparator())

			self.widgets[column_name] = field

		update_button = Submit(
			size_hint=(1, None),
			size=(self.width, 60),
			text=LOCALIZED.translate('Update')
		)
		update_button.bind(on_release=self.apply_change)
		content.add_widget(update_button)

	def get_values(self) -> dict:
		return {w_name: w_value.get_value()\
			for w_name, w_value in self.widgets.items()
		}

	def update_theme(self, values: dict) -> None:
		app = MDApp.get_running_app()

		for palette, color in values.items():
			setattr(app.theme_cls, palette, color)

	@check_db_commit_except
	def save(self, values: dict) -> None:
		self.table.query.filter_by(id=1).update(values)
		db.session.commit()

	def apply_change(self, instance: Submit) -> None:
		values = self.get_values()
		print(values)
		self.update_theme(values)
		self.save(values)