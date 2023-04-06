from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

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