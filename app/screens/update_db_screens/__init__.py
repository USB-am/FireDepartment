# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets import CustomScreen
from app.tools import fields


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'update_db_screens.kv')
Builder.load_file(path_to_kv_file)


class AbstractUpdateDBScreen(CustomScreen):
	def __init__(self):
		super().__init__()

		self.fields = {}

		self.update_title()
		self.update_content()

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate(self.name)
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		content = self.ids.content
		content.clear_widgets()

		for title, field in self.table.get_fields().items():
			try:
				content.add_widget(getattr(fields, field)(title))
			except Exception as error:
				print('[{}] {}'.format(
					error.__class__.__name__,
					str(error)
				))