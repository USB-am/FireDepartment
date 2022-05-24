# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.card import MDSeparator

from app.tools.custom_widgets import CustomScreen
from app.tools import fields as FIELDS
from config import PATTERNS_DIR, LOCALIZED
from data_base import ColorTheme


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_color_theme.kv')
Builder.load_file(path_to_kv_file)


class UpdateColorTheme(CustomScreen):
	name = 'update_color_theme'
	table = ColorTheme

	def __init__(self):
		super().__init__()

		self.update_title()
		self.update_content()

	def update_title(self) -> None:
		self.ids.toolbar.title = LOCALIZED.translate(self.name)

	def update_content(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		current_theme = self.table.query.first()
		table_fields = self.table.get_fields()

		for column_name, field_name in table_fields.items():
			field = getattr(FIELDS, field_name)(column_name)
			field.set_value(getattr(current_theme, column_name))
			content.add_widget(field)
			content.add_widget(MDSeparator())

		update_button = Button(
			size_hint=(1, None),
			size=(self.width, 60),
			text=LOCALIZED.translate('Update')
		)
		update_button.bind(on_release=self.update_theme)
		content.add_widget(update_button)

	def update_theme(self, instance: Button) -> None:
		# TODO: сделать обновление в базе данных
		# 	+ изменить цветовую схему приложения
		pass