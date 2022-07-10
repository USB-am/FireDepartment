# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from config import PATTERNS_DIR, LOCALIZED
from data_base import Emergency
from app.tools.custom_widgets import CustomScreen
from app.tools.fields import ToManyDisplayField


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'emergency.kv')
Builder.load_file(path_to_kv_file)


class EmergencyPage(CustomScreen):
	name = 'emergency_page'
	table = Emergency

	def update_values(self, values: dict) -> None:
		content = self.ids.content
		content.clear_widgets()

		for title, value in values.items():
			if title == 'title':
				print(LOCALIZED.translate(title), value)
			elif title == 'discription':
				print(LOCALIZED.translate(title), value)
			elif title == 'urgent':
				print(LOCALIZED.translate(title), '!' if value else '.')
			elif title == 'humans':
				field = ToManyDisplayField(title, value)
				field.update()
				content.add_widget(field)
			elif title == 'tags':
				print(LOCALIZED.translate(title), list(map(str, value)))