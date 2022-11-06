from kivymd.uix.expansionpanel import MDExpansionPanel

from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype, ColorTheme
from uix import FDExpansionPanel, ExpansionOptionsElement, ExpansionOptionsColorTheme


class Options(CustomScrolledScreen):
	''' Экран настроек '''

	name = 'options'

	def __init__(self, path_manager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Options')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager
			.back())
		self.toolbar.add_right_button('palette', lambda e: self.path_manager
			.forward('global_options'))

	def fill_content(self) -> None:
		for data_base_table in (Tag, Rank, Position, Human, Emergency, Worktype):
			element = FDExpansionPanel(data_base_table, ExpansionOptionsElement)
			element.content.binding(self.path_manager)
			self.add_widgets(element)

		# element = FDExpansionPanel(ColorTheme, ExpansionOptionsColorTheme)
		# element.content.binding(self.path_manager)
		# self.add_widgets(element)