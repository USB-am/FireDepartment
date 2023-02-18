from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel

from . import BaseScrolledScreen
from app.path_manager import PathManager


class MainScreen(BaseScrolledScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.add_widgets(*[MDLabel(text=f'Row #{i}') for i in range(10)])