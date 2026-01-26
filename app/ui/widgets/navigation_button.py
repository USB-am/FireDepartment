from kivymd.app import MDApp
from kivy.metrics import dp, sp
from kivymd.uix.button import MDRectangleFlatIconButton


class NavigationButton(MDRectangleFlatIconButton):
	''' Кнопка, использующаяся в меню навигации '''

	def __init__(self, *args, **kwargs):
		self.__theme_cls = MDApp.get_running_app().theme_cls
		kwargs.update({
			'icon_color': self.__theme_cls.accent_color,
			'halign': 'left',
			'theme_text_color': 'Custom',
			'text_color': self.__theme_cls.accent_color,
			'height': dp(80),
			'font_size': sp(20),
			'line_color': (0, 0, 0, 0),
		})

		super().__init__(*args, **kwargs)
