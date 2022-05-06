# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from app.tools.custom_widgets import CustomScreen
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR
from data_base import Emergency


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'main_page.kv')
Builder.load_file(path_to_kv_file)


class EmergencyElement(MDBoxLayout):
	def __init__(self, element):
		self._element = element

		super().__init__()


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.update_content()

	def filter_emergencies(self, search_text: str) -> list:
		return Emergency.query.all()

	def update_content(self, emergencies: list=Emergency.query.all()) -> None:
		content = self.ids.content
		content.clear_widgets()

		for emergency in emergencies:
			emergency_text = str(emergency)
			emergency_secondary = emergency.description if not None else '-'

			content.add_widget(MDExpansionPanel(
				icon=emergency.icon,
				content = EmergencyElement(emergency),
				panel_cls=MDExpansionPanelTwoLine(
					text=emergency_text,
					secondary_text=emergency_secondary
				)
			))