from os import path

from data_base import Emergency, Human, Tag, Rank, Position
from app.tools.custom_screen import CustomScrolledScreen
from app.tools.addition_elements import OptionListItem


class Options(CustomScrolledScreen):
	name = 'options'

	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())

		tables = (Tag, Rank, Position, Human, Emergency)
		for table in tables:
			self.add_widgets(OptionListItem(table))