# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

from config import PATTERNS_DIR, LOCALIZED
from app.tools.custom_widgets.label import FDLabel


class DialogContent(MDBoxLayout):
	def __init__(self, error: str):
		super().__init__()

		self.add_widget(FDLabel(
			text=error,
			halign='center'
		))


class ExceptionDialog(MDDialog):
	def __init__(self, error):
		self.title = LOCALIZED.translate(error.__class__.__name__)
		self.type = 'custom'
		self.content_cls = DialogContent(str(error))
		self.buttons = [
			MDFlatButton(text='Good')
		]

		super().__init__()