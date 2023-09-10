from kivy.uix.screenmanager import Screen

from .base_screen import BaseScreen


class MainScreen(BaseScreen):
	''' Главный экран '''

	def __init__(self, parent: Screen):
		self.parent = parent

		super().__init__()