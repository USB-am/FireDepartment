# -*- coding: utf-8 -*-

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

from kivy.uix.colorpicker import ColorPicker


class FDDialog(MDDialog):
	def __init__(self, title: str, content: MDBoxLayout):

		self.title = title
		self.content_cls=content
		self.type = 'custom'
		self.buttons = [
			MDFlatButton(text='CANCLE'),
			MDFlatButton(text='OK')
		]

		super().__init__(size_hint=(.9, .9))

	@property
	def ok_button(self) -> MDFlatButton:
		return self.buttons[1]

	@property
	def cancle_button(self) -> MDFlatButton:
		return self.buttons[0]


class FDColorPicker(FDDialog):
	def __init__(self, title: str):
		self.color_picker = ColorPicker(
			size_hint=(1, None),
			size=(self.width, 400)
		)

		super().__init__(title=title, content=self.color_picker)

		self._current_color = None

		self.ok_button.bind(on_release=self.ok_click)

	@property
	def current_color(self) -> list:
		return self._current_color

	@current_color.setter
	def current_color(self, color: list) -> None:
		self._current_color = color
		self.color_picker.color = color

	def ok_click(self, instance: MDFlatButton) -> None:
		self.current_color = self.get_value()
		self.dismiss()

	def get_value(self) -> list:
		return self.color_picker.color