from typing import Callable

from kivy.properties import StringProperty
from kivymd.uix.toolbar import MDToolbar

class FDToolbar(MDToolbar):
	''' Верхняя полоска '''

	def add_left_button(self, icon: str, callback: Callable) -> None:
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback: Callable) -> None:
		self.right_action_items.append([icon, callback])
