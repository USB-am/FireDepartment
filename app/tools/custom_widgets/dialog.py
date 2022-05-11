# -*- coding: utf-8 -*-

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton


class FDDialog(MDDialog):
	def __init__(self, title: str, content: MDBoxLayout,\
				size_hint: tuple=(.9, .9)):

		self.title = title
		self.content_cls=content
		self.type = 'custom'
		self.buttons = [
			MDFlatButton(text='CANCLE'),
			MDFlatButton(text='OK')
		]

		super().__init__()

	@property
	def ok_button(self) -> MDFlatButton:
		return self.buttons[1]

	@property
	def cancle_button(self) -> MDFlatButton:
		return self.buttons[0]