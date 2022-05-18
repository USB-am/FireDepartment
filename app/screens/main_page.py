# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout

from app.tools.custom_widgets import CustomScreen, FDExpansionPanel
from config import PATTERNS_DIR, LOCALIZED
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

		self.bind(on_pre_enter=lambda x: self.update_content())

		self.update_title()

	def filter_emergencies(self, search_text: str) -> list:
		return Emergency.query.all()

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate('Emergency')
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		emergencies = Emergency.query.all()

		if not emergencies:
			return

		content = self.ids.content
		content.clear_widgets()

		for emergency in emergencies:
			content.add_widget(FDExpansionPanel(
				db_model=emergency,
				content=EmergencyElement,
				text=(
					emergency.title,
					str(emergency.description)
				)
			))