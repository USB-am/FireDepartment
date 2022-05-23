# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from app.tools.custom_widgets import CustomScreen
from app.tools import fields
from config import PATTERNS_DIR, LOCALIZED
from data_base import ColorTheme


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_color_theme.kv')
Builder.load_file(path_to_kv_file)


color_names = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue',
	'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow',
	'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
colors_data = {
	'theme': color_names,
	'accent': color_names,
	'hue': ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900',
		'A100', 'A200', 'A400', 'A700']
}


class UpdateColorTheme(CustomScreen):
	name = 'update_color_theme'
	table = ColorTheme

	def __init__(self):
		super().__init__()

		self.update_content()

	def update_content(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		table_fields = self.table.get_fields()

		for column_name, field_name in table_fields.items():
			data = colors_data.get(column_name, [])
			field = getattr(fields, field_name)(column_name, data)
			content.add_widget(field)