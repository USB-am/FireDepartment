from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout

from config import APP_SCREEN, APP_ICON
from .path_manager import PathManager
from ui.screens.main import MainScreen
from ui.screens.options import OptionsScreen
from ui.screens.calls import CallsScreen
from ui.screens.history import History
from ui.screens.model_list import TagsList, RanksList, PositionsList, \
	HumansList, EmergenciesList, WorktypesList, ShortsList
from ui.screens.model_create import TagCreateModel, RankCreateModel, \
	PositionCreateModel, HumanCreateModel, WorktypeCreateModel, \
	EmergencyCreateModel, ShortCreateModel
from ui.screens.model_edit import TagEditModel, RankEditModel, \
	PositionEditModel, HumanEditModel, EmergencyEditModel, \
	WorktypeEditModel, ShortEditModel


Builder.load_file(APP_SCREEN)


class FDUIManager(MDNavigationLayout):
	''' Графический интерфейс приложения. '''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.path_manager = PathManager(self.screen_manager)

		self.ids.main_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('main'))
		self.ids.options_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('options'))
		self.ids.tags_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('tags_list'))
		self.ids.shorts_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('shorts_list'))
		self.ids.ranks_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('ranks_list'))
		self.ids.positions_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('positions_list'))
		self.ids.humans_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('humans_list'))
		self.ids.emergencies_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('emergencies_list'))
		self.ids.worktype_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('worktypes_list'))
		self.ids.history_nav_btn.bind(on_release=lambda *_:
			self.move_screen_and_close_menu('history'))

	def move_screen_and_close_menu(self, screen_name: str) -> None:
		'''
		Перенаправляет на screen_name страницу и закрывает меню.

		~params:
		screen_name: str - имя страницы.
		'''

		self.path_manager.move_to_screen(screen_name)
		self.ids.menu.set_state('close')

	@property
	def screen_manager(self) -> ScreenManager:
		return self.ids.screen_manager


class Application(MDApp):
	'''
	Базовый класс приложения. Инициализирует интерфейс и добавляет страницы.
	'''

	icon = APP_ICON
	title = 'Fire Department'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ui = FDUIManager()

		self.ui.screen_manager.add_widget(CallsScreen(self.ui.path_manager))
		self.ui.screen_manager.add_widget(MainScreen(self.ui.path_manager))
		self.ui.screen_manager.add_widget(OptionsScreen(self.ui.path_manager))
		self.ui.screen_manager.add_widget(History(self.ui.path_manager))
		# Model list screens
		self.ui.screen_manager.add_widget(TagsList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(RanksList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(PositionsList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(HumansList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(EmergenciesList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(WorktypesList(self.ui.path_manager))
		self.ui.screen_manager.add_widget(ShortsList(self.ui.path_manager))
		# Create model screens
		self.ui.screen_manager.add_widget(TagCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(RankCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(PositionCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(HumanCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(EmergencyCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(WorktypeCreateModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(ShortCreateModel(self.ui.path_manager))
		# Edit model screens
		self.ui.screen_manager.add_widget(TagEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(RankEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(PositionEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(HumanEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(EmergencyEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(WorktypeEditModel(self.ui.path_manager))
		self.ui.screen_manager.add_widget(ShortEditModel(self.ui.path_manager))

		self.ui.path_manager.move_to_screen('main')

	def build_config(self, config):
		config.setdefaults('options', {
			'primary_palette': self.theme_cls.primary_palette,
			'accent_palette': self.theme_cls.accent_palette,
			'theme_style': self.theme_cls.theme_style,
			'primary_hue': self.theme_cls.primary_hue,
		})
		config.setdefaults('call', {
			'work_day_ignore': '1',
			'start_text': '[HH:MM dd.mm.yyyy] Начало выезда.',
			'finish_text': '[HH:MM dd.mm.yyyy] Конец выезда.',
			'human_success': '[HH:MM dd.mm.yyyy] Вызов {human_name}.',
			'human_unsuccess': '[HH:MM dd.mm.yyyy] Вызов {human_name} не прошел.',
		})

	def build(self):
		config = self.config
		self.theme_cls.primary_palette = config.get('options', 'primary_palette')
		self.theme_cls.accent_palette = config.get('options', 'accent_palette')
		self.theme_cls.theme_style = config.get('options', 'theme_style')
		self.theme_cls.primary_hue = config.get('options', 'primary_hue')

		return self.ui
