from config import LOCALIZED, path_manager
from app.tools import CustomScreen
from data_base import db, Emergency
from app.tools.addition_elements import MainPageListElement


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('fire-truck', lambda e: print(
			path_manager.PathManager().current))
		self.toolbar.add_right_button('cog', lambda e: print(
			path_manager.PathManager().current))

		# self.add_widgets(FDSwitch('Content'), FDSwitch('Human'))
		for row in Emergency.query.all()[:10]:
			self.add_widgets(MainPageListElement(row))