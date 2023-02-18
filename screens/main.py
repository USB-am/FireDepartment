from kivy.lang.builder import Builder

from . import BaseScreen
from app.path_manager import PathManager
from config import paths


Builder.load_file(paths.MAIN_SCREEN)


class MainScreen(BaseScreen):
	''' Главная страница '''

	name = 'main'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager