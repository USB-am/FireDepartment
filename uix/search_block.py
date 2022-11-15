from typing import Union

from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from sqlalchemy import func

from config import LOCALIZED
from data_base import db, Emergency, Tag


class SearchTextField(MDTextField):
	''' Текстовое поля блока поиска '''

	def __init__(self, **options):
		super().__init__(**options)

		self.callback = lambda: None

	def binding(self, callback) -> None:
		self.callback = callback

	def on_text(self, instance, value):
		self.callback()


class FDSearchBlock(MDBoxLayout):
	''' Блок поиска '''

	def __init__(self):
		super().__init__(
			orientation='horizontal',
			size_hint=(1, None),
			size=(self.width, 50))

		self.entry = SearchTextField(
			size_hint=(1, 1),
			hint_text=LOCALIZED.translate('Search'))
		self.delete_button = MDIconButton(
			size_hint=(None, None),
			size=(50, 50),
			icon='close')

		self.add_widget(self.entry)
		self.add_widget(self.delete_button)


class EmergencySearchBlock(FDSearchBlock):
	''' Блок поиска ЧС '''

	def _sorted_by_name(self, elements: Union[set, list]) -> list:
		return sorted(elements, key=lambda el: el.title)

	def filter(self) -> list:
		search_text = self.entry.text

		if not search_text:
			return self._sorted_by_name(Emergency.query.all())

		like_search_text = f'%{search_text}%'
		found_tags = self._filter_from_tags(like_search_text)
		found_emergencies = self._filter_from_emergencies(like_search_text)
		finded_emergencies = set([*found_tags, *found_emergencies])

		sorted_elements = self._sorted_by_name(finded_emergencies)

		return sorted_elements

	def _filter_from_tags(self, like_search_text: str) -> list:
		tags = Tag.query.filter(Tag.title.like(like_search_text))
		emergencies = []
		[emergencies.extend(tag.emergencys) for tag in tags]

		return emergencies

	def _filter_from_emergencies(self, like_search_text: str) -> list:
		return Emergency.query.filter(Emergency.title.ilike(like_search_text))