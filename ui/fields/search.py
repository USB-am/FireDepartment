from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

from config.paths import SEARCH_FIELD
from .entry import FDTextInput


Builder.load_file(SEARCH_FIELD)


class FDSearch(MDBoxLayout):
	''' Поле для поиска '''

	def __init__(self):
		super().__init__()

		self.search_text = MDTextField(
			hint_text='Search...'
		)
		self.search_btn = MDIconButton(icon='magnify')

		self.add_widget(self.search_text)
		self.add_widget(self.search_btn)

	def bind_on_enter(self, callback) -> None:
		self.search_text.bind(
			on_text_validate=lambda e: callback()
		)
		self.search_btn.bind(
			on_release=lambda e: callback()
		)

	@property
	def text(self) -> str:
		return self.search_text.text

	@text.setter
	def text(self, text: str) -> None:
		self.search_text.text = text