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


class EmergenciesFilter:
	__current = ''

	@property
	def current(self) -> list:
		if self.__current == '':
			return self.all()
		else:
			return []

	@current.setter
	def current(self, search_text: str) -> None:
		self.__current = search_text

	def all(self) -> list:
		return Emergency.query.all()

	def filter_(self, tag: str) -> list:
		return []


class EmergencyElement(MDBoxLayout):
	def __init__(self, element):
		self._element = element

		super().__init__()


class MainPage(CustomScreen):
	name = 'main_page'
	filters = EmergenciesFilter()

	def __init__(self):
		super().__init__()

		self.update_title()

		self.bind(on_pre_enter=lambda x: self.update_content())
		self.ids.search_block.text_field.bind(
			on_text_validate=lambda x: self.search())
		self.ids.search_block.search_button.bind(
			on_release=lambda x: self.search())

	def search(self) -> None:
		self.filters.current = self.ids.search_block.text_field.text

	def view_posts(self, emergencies: list) -> None:
		for emergency in emergencies:
			self.ids.content.add_widget(
				FDExpansionPanel(
					db_model=emergency,
					content=EmergencyElement,
					text=(emergency.title, str(emergency.description))
			))

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate('Emergency')
		self.ids.toolbar.title = translate_text

	def update_content(self) -> None:
		emergencies = Emergency.query.all()

		if not emergencies:
			return

		content = self.ids.content
		content.clear_widgets()

		self.view_posts(self.filters.current)