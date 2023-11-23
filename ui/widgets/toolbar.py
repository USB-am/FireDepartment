from typing import Callable

from kivy.lang.builder import Builder
from kivymd.uix.toolbar import MDToolbar


Builder.load_string('''
<FDToolbar>:
	md_bg_color: app.theme_cls.accent_color
''')


class FDToolbar(MDToolbar):
	''' Верхняя полоска '''

	def add_left_button(self, icon: str, callback: Callable) -> None:
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback: Callable) -> None:
		self.right_action_items.append([icon, callback])