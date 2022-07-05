# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.boxlayout import MDBoxLayout

from app.tools.custom_widgets import CustomScreen, FDExpansionPanel
from config import PATTERNS_DIR, LOCALIZED
from data_base import db, Emergency, Tag


path_to_kv_file = os.path.join(PATTERNS_DIR, 'screens', 'main_page.kv')
Builder.load_file(path_to_kv_file)


class EmergenciesFilter:
	__current = ''

	@property
	def current(self) -> tuple:
		if self.__current == '':
			return self.all()
		else:
			return self.filter_()

	@current.setter
	def current(self, search_text: str) -> None:
		self.__current = search_text

	def all(self) -> tuple:
		return tuple(Emergency.query.all())

	def filter_(self) -> tuple:
		def sort_by_id(elements: tuple) -> tuple:
			return sorted(elements, key=lambda element: element.id)

		elements_set = set()
		# 'tag #1, tag #2 ,  tg#N' -> ('tag #1', 'tag #2', 'tg#N')
		search_elements = tuple(map(
			lambda x: x.strip(), self.__current.split(',')))

		for tag in search_elements:
			questions = Tag.query.filter(Tag.title.like(f'%{tag}%'))

			emergencies = tuple(map(lambda tag: tag.emergencys, questions))
			# ([...], [...], [...]) -> [.........]
			elements = [item for sublist in emergencies for item in sublist]
			elements_set |= set(elements)

		found_elements = tuple(elements_set)

		return sort_by_id(found_elements)


class EmergencyInfoBlock(MDBoxLayout):
	def __init__(self, icon: str, value: int):
		self.icon = icon
		self.value = value
		self.text = '' if icon == 'truck-fast' else str(value)

		super().__init__()


class EmergencyElement(MDBoxLayout):
	def __init__(self, element):
		self._element = element

		super().__init__()

		self._fill_info_row()

	def _fill_info_row(self) -> None:
		values = {
			'urgent': ('truck-fast', self._element.urgent),
			'humans': ('account-group', len(self._element.humans)),
			'tags': ('pound', len(self._element.tags))
		}

		for item, (icon, value) in values.items():
			if item == 'urgent' and not value:
				continue

			self.ids.info_row.add_widget(EmergencyInfoBlock(icon, int(value)))

	def get_values(self) -> dict:
		return {field: getattr(self._element, field)\
			for field in self._element.get_fields().keys()}


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
		self.update_content(self.filters.current)

	def clear_content(self) -> None:
		self.ids.content.clear_widgets()

	def update_title(self) -> None:
		translate_text = LOCALIZED.translate('Emergency')
		self.ids.toolbar.title = translate_text

	def update_content(self, emergencies: list=None) -> None:
		if emergencies is None:
			emergencies = self.filters.current

		self.clear_content()

		for emergency in emergencies:
			self.ids.content.add_widget(
				FDExpansionPanel(
					db_model=emergency,
					content=EmergencyElement,
					text=(emergency.title, str(emergency.description))
			))