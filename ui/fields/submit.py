from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton

from config import paths


Builder.load_file(paths.SUBMIT_BUTTON)


class FDSubmit(MDBoxLayout):
	''' Кнопка отправки формы '''

	def __init__(self, text: str):
		self._text = text
		self.__callback = None

		super().__init__()

	@property
	def text(self) -> str:
		return self._text

	@text.setter
	def text(self, value: str) -> None:
		self._text = value
		self.ids.btn.text = value

	def bind_btn(self, callback) -> None:
		self.ids.btn.unbind(on_release=self.__callback)
		self.__callback = callback
		self.ids.btn.bind(on_release=self.__callback)