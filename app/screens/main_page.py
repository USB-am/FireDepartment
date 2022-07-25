from config import LOCALIZED, path_manager
from app.tools import CustomScreen
from data_base import db, Emergency
from app.tools.addition_elements import MainPageListElement


class MainPage(CustomScreen):
	name = 'main_page'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('fire-truck', lambda e: \
			self.path_manager_.forward('fires'))
		self.toolbar.add_right_button('cog', lambda e: print(
			self.path_manager_.current))

		self.bind(on_pre_enter=self.fill_emergencies)

	def fill_emergencies(self, event) -> None:
		super().clear_scroll_content()

		for row in Emergency.query.all()[:10]:
			self.add_widgets(MainPageListElement(row))