from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import COLORS_FIELD
from ui.frames.dialogs import FDDialog
from ui.frames.dialogs.color_content import ColorDialogContent


Builder.load_file(COLORS_FIELD)


class FDColor(MDBoxLayout):
	''' Поле выбора цвета из палитры '''

	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title

		super().__init__()

		self._dialog = None

	def open_dialog(self) -> None:
		if self._dialog is None:
			self.color_content = ColorDialogContent()
			self._dialog = FDDialog(
				title=self.title,
				content=self.color_content
			)
			self._dialog.ok_button.bind(
				on_release=lambda e: self.update_button_color()
			)

		self._dialog.open()

	def update_button_color(self) -> None:
		color = self.color_content.get_value()
		self.ids.btn.md_bg_color = color

	def get_value(self) -> list:
		return self.color_content.get_value()

	def set_value(self, color: list) -> None:
		self.color_content.set_value(color)