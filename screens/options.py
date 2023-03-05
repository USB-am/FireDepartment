from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel

from data_base import Tag, Rank, Position, Human, Emergency
from . import BaseScrolledScreen
from app.path_manager import PathManager
from ui.frames.list_items import FDOptionsListItem


class OptionsScreen(BaseScrolledScreen):
	''' Главная страница '''

	name = 'options'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager
		self.__fill_toolbar()
		self.__fill_content()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda event: self.path_manager.back()
		)
		self.toolbar.add_right_button(
			icon='palette',
			callback=lambda event: self.path_manager.forward('color_theme_edit')
		)

	def __fill_content(self) -> None:
		models = (Tag, Rank, Position, Human, Emergency,)
		items = []

		for model in models:
			item = FDOptionsListItem(model)
			items.append(item)

		self.add_widgets(*items)