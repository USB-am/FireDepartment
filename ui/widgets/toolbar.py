from kivymd.uix.toolbar import MDToolbar

from config.localizer import LOCALIZE


class FDToolbar(MDToolbar):
	''' Верхняя понель на экране '''

	def __init__(self, title: str):
		self.title = LOCALIZE(title).capitalize()
		super().__init__()

	def add_left_button(self, icon: str, callback) -> None:
		''' Добавит иконку слева '''
		self.left_action_items.append([icon, callback])

	def add_right_button(self, icon: str, callback) -> None:
		''' Добавит иконку справа '''
		self.right_action_items.append([icon, callback])