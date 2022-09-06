from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config import LOCALIZED
from data_base import db, Emergency, Tag


class SearchTextField(MDTextField):
	''' Текстовое поля блока поиска '''

	def __init__(self, **options):
		super().__init__(**options)

		self.callback = lambda: None

	def binding(self, callback) -> None:
		self.callback = callback

	def insert_text(self, substring: str, from_undo: bool=False) -> None:
		super().insert_text(substring, from_undo=from_undo)

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

	def _sorted_by_id(self, elements: set) -> list:
		return sorted(elements, key=lambda el: el.id)

	def filter(self) -> list:
		search_text = self.entry.text

		if not search_text:
			return Emergency.query.all()

		output = set()
		like_search_text = f'%{search_text}%'
		found_tags = Tag.query.filter(Tag.title.like(like_search_text))

		for found_tag in found_tags:
			[output.add(emergency) for emergency in found_tag.emergencys]

		return self._sorted_by_id(output)