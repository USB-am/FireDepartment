from . import BaseScreen
from app.path_manager import PathManager
from data_base import Emergency


class CurrentCallsScreen(BaseScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()

	def add_tab(self, entry: Emergency):
		print(f'Add tag {entry.title}')