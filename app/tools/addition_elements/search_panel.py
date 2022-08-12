from os import path

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField

from config import ADDITION_ELEMENTS_DIR, LOCALIZED


path_to_kv_file = path.join(ADDITION_ELEMENTS_DIR, 'search_panel.kv')
Builder.load_file(path_to_kv_file)


class SearchPanel(MDBoxLayout):
	''' Набор виджетов для поиска '''
	_placeholder = LOCALIZED.translate('search')

	def __init__(self, *a, **kw):
		super().__init__(*a, **kw)

		self.ids.clear_content_btn.bind(
			on_release=lambda e: self.clear_entry())

	def clear_entry(self) -> None:
		self.ids.search_entry.text = ''