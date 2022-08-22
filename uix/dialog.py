import os

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

from config import UIX_KV_DIR
from data_base import Human


path_to_kv_file = os.path.join(UIX_KV_DIR, 'dialog.kv')
Builder.load_file(path_to_kv_file)


class FDDialog(MDDialog):
	''' Всплывающее окно '''

	def __init__(self, title: str, content: MDBoxLayout,
	             buttons: list[MDFlatButton]=[], **options):

		self.title = title
		self.content_cls = content
		self.type = 'custom'
		self.buttons = buttons

		super().__init__(**options)


class HumanDialogContent(MDBoxLayout):
	''' Всплывающее окно с информацией о человеке '''

	def __init__(self, human: Human):
		self.human = human
		# self.title = human.title

		super().__init__()