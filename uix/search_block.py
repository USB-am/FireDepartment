from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config import LOCALIZED
from data_base import db


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

	def __init__(self, table: db.Model):
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

		self.table = table
		self.elements = self.table.query.all()

	def filter(self) -> list:
		search_text = self.entry.text
		like_search_text = f'%{self.entry.text}%'
		print(like_search_text, search_text)

		if search_text:
			output = self.table.query.filter(
				self.table.tags.title.like(like_search_text)
				).all()
		else:
			output = self.table.query.all()

		return output