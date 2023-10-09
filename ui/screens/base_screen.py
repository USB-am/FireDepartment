from os.path import join as pjoin

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatIconButton

from config.paths import __SCREENS_DIR
from app.path_manager import PathManager


Builder.load_file(pjoin(__SCREENS_DIR, 'base_screen.kv'))


class NavigationButton(MDRectangleFlatIconButton):
	""" Кнопка, использующаяся в меню навигации """

	theme_cls = ThemeManager()

	def __init__(self, *args, **kwargs):
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

		self.display()

	def open_menu(self, *events) -> None:
		self.ids.menu.set_state('open')

	def add_content(self, widget) -> None:
		self.ids.content.add_widget(widget)

	def display(self) -> None:
		pass