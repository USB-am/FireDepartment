from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField

from config import LOCALIZED


class SearchEntry(MDTextField):
	''' Текстовое поле запускающее событие при вводе '''
	def __init__(self, callback=None, **options):
		super().__init__(**options)

		self.callback = callback

	def insert_text(self, substring: str, from_undo: bool=False):
		super().insert_text(substring, from_undo=from_undo)

		if self.callback is not None:
			return self.callback()
		return


class SearchPanel(MDBoxLayout):
	''' Набор виджетов для поиска '''
	_placeholder = LOCALIZED.translate('Search')

	def __init__(self):
		super().__init__(size_hint=(1, None), size=(self.width, 35))

		self.__init_ui()
		self.__binding()

	def __init_ui(self) -> None:
		self.entry = SearchEntry(hint_text=self._placeholder)
		self.button = MDIconButton(
			size_hint=(None, None),
			size=(35, 35),
			icon='close')

		self.add_widget(self.entry)
		self.add_widget(self.button)

	def __binding(self) -> None:
		self.button.bind(on_release=lambda e: self.clear_entry())

	def clear_entry(self) -> None:
		self.entry.text = ''