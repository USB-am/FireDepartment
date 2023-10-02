from os.path import join as pjoin

from kivy.lang.builder import Builder
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatIconButton

from app.path_manager import PathManager
# from ui.widgets.toolbar import Toolbar
from config.paths import __SCREENS_DIR


Builder.load_file(pjoin(__SCREENS_DIR, 'base_screen.kv'))


class NavigationButton(MDRectangleFlatIconButton):
	""" Кнопка, использующаяся в меню навигации """

	theme_cls = ThemeManager()

	def __init__(self, *args, **kwargs):
		print(dir(self.theme_cls))
		kwargs.update({
			'theme_text_color': 'Custom',
			'icon_color': self.theme_cls.accent_dark,
			'text_color': self.theme_cls.text_color,
			'height': dp(80),
			'font_size': sp(20),
			'line_color': (0, 0, 0, 0),
		})

		super().__init__(*args, **kwargs)


class BaseScreen(Screen):
	""" Базовый класс страницы """

	color = [1, 1, 1, 1]
	bg_image = None

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.__path_manager = path_manager


class MainScreen(BaseScreen):
	""" Главная страница """

	name = 'main'
	toolbar_title = 'Главная'

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)