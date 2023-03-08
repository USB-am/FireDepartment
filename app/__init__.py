from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .path_manager import PathManager
from screens.main import MainScreen
from screens.options import OptionsScreen
from screens.edit_model_list import EditTagListScreen, EditRankListScreen, \
	EditPositionListScreen, EditHumanListScreen, EditEmergencyListScreen


class Application(MDApp):
	'''
	Главный класс приложения
	'''

	def __init__(self):
		super().__init__()
		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.__add_screens()

	def __add_screens(self) -> None:
		self.main_screen = MainScreen(self.path_manager)
		self.screen_manager.add_widget(self.main_screen)

		self.options_screen = OptionsScreen(self.path_manager)
		self.screen_manager.add_widget(self.options_screen)

		self.edit_tag_list_screen = EditTagListScreen(self.path_manager)
		self.screen_manager.add_widget(self.edit_tag_list_screen)

		self.edit_rank_list_screen = EditRankListScreen(self.path_manager)
		self.screen_manager.add_widget(self.edit_rank_list_screen)

		self.edit_position_list_screen = EditPositionListScreen(self.path_manager)
		self.screen_manager.add_widget(self.edit_position_list_screen)

		self.edit_human_list_screen = EditHumanListScreen(self.path_manager)
		self.screen_manager.add_widget(self.edit_human_list_screen)

		self.edit_emergency_list_screen = EditEmergencyListScreen(self.path_manager)
		self.screen_manager.add_widget(self.edit_emergency_list_screen)

		self.screen_manager.current = 'options'

	def build(self) -> ScreenManager:
		return self.screen_manager