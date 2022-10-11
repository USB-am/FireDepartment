import os

from kivy.lang import Builder
from kivy.uix.colorpicker import ColorPicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

from config import LOCALIZED, FIELDS_KV_DIR
from uix.dialog import FDDialog


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'color.kv')
Builder.load_file(path_to_kv_file)


class ColorDialog(FDDialog):
	''' Всплавающее окно с выбором цвета '''

	def __init__(self, callback=None):
		self.callback = callback

		self.display_title = LOCALIZED.translate('Color selection.')

		content = MDBoxLayout()
		content.add_widget(ColorPicker())

		ok_button = MDRaisedButton(text=LOCALIZED.translate('Ok'))
		ok_button.bind(on_release=self._dismiss_and_callback)
		cancle_button = MDRaisedButton(text=LOCALIZED.translate('Cancel'))
		cancle_button.bind(on_release=lambda e: self.dismiss())

		super().__init__(
			self.display_title,
			content,
			[ok_button, cancle_button],
			size_hint=(.9, None),
			size=(self.width, 400)
		)

	def _dismiss_and_callback(self, event):
		self.dismiss()
		# self.callback()


class FDColor(MDBoxLayout):
	''' Виджет для выбора цвета '''

	def __init__(self, icon: str, title: str):
		self.icon = icon
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		self.color_dialog = ColorDialog()

		super().__init__()

	def open_picker(self) -> None:
		self.color_dialog.open()