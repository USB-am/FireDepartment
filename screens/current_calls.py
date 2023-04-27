from . import BaseScrolledScreen, BaseScreen
from app.path_manager import PathManager
from data_base import Emergency
from ui.fields.switch import FDTripleCheckbox
from ui.widgets.notebook import FDNotebook


# class CurrentCallsScreen(BaseScrolledScreen):
# 	''' Экран текущих вызовов '''

# 	name = 'current_calls'

# 	def __init__(self, path_manager: PathManager):
# 		self.path_manager = path_manager

# 		super().__init__()

# 		self.__fill_toolbar()

# 	def __fill_toolbar(self) -> None:
# 		self.toolbar.add_left_button(
# 			icon='arrow-left',
# 			callback=lambda e: self.path_manager.back()
# 		)

# 	def add_tab(self, entry: Emergency):
# 		humans = entry.humans

# 		for human in humans:
# 			self.add_widgets(FDTripleCheckbox(
# 				title=human.title,
# 				substring=human.phone_1
# 			))


class CurrentCallsScreen(BaseScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()

		self.__fill_toolbar()

		self.notebook = FDNotebook()
		self.add_widgets(self.notebook)

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def add_tab(self, entry: Emergency):
		pass