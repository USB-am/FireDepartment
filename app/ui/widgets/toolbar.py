from typing import Callable

from kivymd.uix.toolbar import MDTopAppBar


class FDToolbar(MDTopAppBar):
	''' Верхняя полоска '''

	def add_left_button(self, icon: str, callback: Callable) -> None:
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback: Callable) -> None:
		self.right_action_items.append([icon, callback])

	def rem_left_button(self) -> None:
		self.left_action_items.pop()

	def rem_right_button(self) -> None:
		self.right_action_items.pop()
