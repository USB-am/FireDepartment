from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .path_manager import PathManager
from screens.main import MainScreen
from screens.current_calls import CurrentCallsScreen
from screens.options import OptionsScreen
from screens.create_model import CreateTagScreen, CreateRankScreen, \
	CreatePositionScreen, CreateHumanScreen, CreateEmergencyScreen, \
	CreateWorktypeScreen
from screens.edit_model_list import EditTagListScreen, EditRankListScreen, \
	EditPositionListScreen, EditHumanListScreen, EditEmergencyListScreen, \
	EditWorktypeListScreen
from screens.edit_model import EditTagScreen, EditRankScreen, \
	EditPositionScreen, EditHumanScreen, EditEmergencyScreen, EditWorktypeScreen
from screens.edit_color_theme import EditColorTheme


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

		self.current_calls = CurrentCallsScreen(self.path_manager)
		self.screen_manager.add_widget(self.current_calls)

		self.edit_color_theme = EditColorTheme(self.path_manager)
		self.screen_manager.add_widget(self.edit_color_theme)

		# Create screens
		_create_screens_objects = (CreateTagScreen, CreateRankScreen,
			CreatePositionScreen, CreateHumanScreen, CreateEmergencyScreen,
			CreateWorktypeScreen)

		for create_screen in _create_screens_objects:
			scr = create_screen(self.path_manager)
			self.screen_manager.add_widget(scr)

		# Edit list screens
		_edit_list_screen_objects = (EditTagListScreen, EditRankListScreen,
			EditPositionListScreen, EditHumanListScreen,
			EditEmergencyListScreen, EditWorktypeListScreen,
		)

		for edit_list_screen in _edit_list_screen_objects:
			scr = edit_list_screen(self.path_manager)
			self.screen_manager.add_widget(scr)

		# Edit screens
		_edit_screens_objects = (EditTagScreen, EditRankScreen,
			EditPositionScreen, EditHumanScreen, EditEmergencyScreen,
			EditWorktypeScreen)

		for edit_screen in _edit_screens_objects:
			scr = edit_screen(self.path_manager)
			self.screen_manager.add_widget(scr)

		self.screen_manager.current = 'main'

	def build(self) -> ScreenManager:
		return self.screen_manager