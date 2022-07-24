from config import LOCALIZED, path_manager
from app.tools import CustomScreen
from data_base import db, Emergency


class Fires(CustomScreen):
	name = 'fires'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: print(
			path_manager.PathManager().back()))
		self.toolbar.add_right_button('check-outline', lambda e: print(
			'call is finished!'))