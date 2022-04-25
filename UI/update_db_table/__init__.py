# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from settings import settings as Settings
from settings import LANG
from UI.custom_screen import CustomScreen
from UI import fields as Fields


path_to_kv_file = os.path.join(Settings.PATTERNS_DIR, 'update_db_table.kv')
Builder.load_file(path_to_kv_file)


class AbstractPage(CustomScreen):
	def __init__(self):
		super().__init__()

		self.widgets = []

		self.bind(on_pre_enter=self.update_screen)

	def update_screen(self, instance: CustomScreen=None) -> None:
		self.ids.toolbar.title = self.table.__tablename__

		container = self.ids.container
		container.clear_widgets()

		fields = self.table.get_fields()

		for title, field_name in fields.items():
			try:
				field_obj = getattr(Fields, field_name)
				widget = field_obj(title=title)
				container.add_widget(widget)
				self.widgets.append(widget)
			except AttributeError as e:
				print(f'[{title}] {field_name} is not found!\n{e}')
				# pass