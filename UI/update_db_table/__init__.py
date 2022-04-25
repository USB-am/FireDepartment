# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDRectangleFlatButton

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
			field_obj = getattr(Fields, field_name)
			widget = field_obj(title=title)
			container.add_widget(widget)
			self.widgets.append(widget)

		submit_button = MDRectangleFlatButton(
			text='Create',
			size_hint=(1, None),
			size=(self.width, 100)
		)
		submit_button.bind(on_press=self.submit)
		container.add_widget(submit_button)

	def submit(self, instance: MDRectangleFlatButton) -> None:
		pass