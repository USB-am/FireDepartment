from . import BaseScreen
from app.path_manager import PathManager


class CurrentCallsScreen(BaseScreen):
	''' Экран текущих вызовов '''

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()