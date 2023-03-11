from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton

from config import paths


Builder.load_file(paths.SUBMIT_BUTTON)


class FDSubmit(MDBoxLayout):
	''' Кнопка отправки формы '''

	def __init__(self, text: str):
		self.text = text

		super().__init__()

	def bind_btn(self, callback) -> None:
		self.ids.btn.bind(on_release=callback)