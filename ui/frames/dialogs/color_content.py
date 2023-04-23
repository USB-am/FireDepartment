from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import COLOR_CONTENT_DIALOG


Builder.load_file(COLOR_CONTENT_DIALOG)


class ColorDialogContent(MDBoxLayout):
	''' Содержимое диалога выбора цвета '''

	def __init__(self):
		super().__init__()

		self._color = [1, 1, 1, 1]
		self.ids.color_picker.bind(
			color=lambda inst, value: self.set_value(value)
		)

	def get_value(self) -> list:
		return self._color

	def set_value(self, color: list) -> None:
		self._color = color
		self.ids.color_picker.color = self._color