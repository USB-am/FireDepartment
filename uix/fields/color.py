import os

from kivy.lang import Builder
from kivy.uix.colorpicker import ColorPicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

from uix.dialog import FDDialog
from uix.help_button import HelpButton
from config import LOCALIZED, FIELDS_KV_DIR, HELP_MODE


path_to_kv_file = os.path.join(FIELDS_KV_DIR, 'color.kv')
Builder.load_file(path_to_kv_file)


class ColorDialog(FDDialog):
	''' Всплавающее окно с выбором цвета '''

	def __init__(self, callback=None):
		self.callback = callback

		self.display_title = LOCALIZED.translate('Color selection.')

		self.picker = ColorPicker()
		content = MDBoxLayout(
			size_hint=(1, None),
			size=(self.width, 400))
		content.add_widget(self.picker)

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

		if self.callback is not None:
			self.callback(self.picker.color)


class FDColor(MDBoxLayout):
	''' Виджет для выбора цвета '''

	def __init__(self, icon: str, title: str, on_color=None, help_text: str=None):
		self.icon = icon
		self.title = title
		self.on_color = on_color
		self.display_text = LOCALIZED.translate(title)

		self._value = [1.0, 1.0, 1.0, 1.0]

		self.color_dialog = ColorDialog(self.change_current_color)

		super().__init__()

		if help_text is not None and HELP_MODE:
			self.ids.label.add_widget(HelpButton(
				title=self.__class__.__name__,
				text=help_text
			))

	@property
	def value(self) -> list:
		return self._value

	@value.setter
	def value(self, color: list) -> None:
		self._value = color
		self.color_dialog.picker.color = color

	def change_current_color(self, color: list) -> None:
		self.set_value(color)
		self.ids.button.md_bg_color = color

		if self.on_color is not None:
			self.on_color(color)

	def get_value(self) -> list:
		return self.value

	def set_value(self, value: list) -> None:
		self.value = value