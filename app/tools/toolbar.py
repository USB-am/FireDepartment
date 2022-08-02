from os import path

from kivy.lang import Builder
from kivymd.uix.toolbar import MDToolbar

from config import TOOLS_DIR, LOCALIZED


path_to_kv_file = path.join(TOOLS_DIR, 'toolbar.kv')
Builder.load_file(path_to_kv_file)


class FDToolbar(MDToolbar):
	''' Верхняя панель '''
	def __init__(self, title: str):
		self.title = title
		self.left_buttons = []
		self.right_buttons = []

		self.display_title = LOCALIZED.translate(title)

		super().__init__()

	def add_left_button(self, icon: str, callback) -> None:
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback) -> None:
		self.right_action_items.append([icon, callback])