from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField

from config.paths import SEARCH_FIELD
from .entry import FDTextInput


Builder.load_file(SEARCH_FIELD)


class FDSearch(MDBoxLayout):
	''' Поле для поиска '''

	def __init__(self):
		super().__init__()

		self.search_text = FDTextInput(
			hint_text='Search...'
		)
		self.ids.text_input_container.add_widget(self.search_text)

	def bind_on_enter(self, callback) -> None:
		self.search_text.entry.bind(
			on_text_validate=lambda e: callback()
		)
		self.ids.search_btn.bind(
			on_release=lambda e: callback()
		)

	@property
	def text(self) -> str:
		return self.search_text.get_value()