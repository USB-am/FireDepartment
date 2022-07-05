# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder

from config import PATTERNS_DIR
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
			if title == 'humans':
				w = ToManyDisplayField(title)
				w.update(value)

				content.add_widget(w)