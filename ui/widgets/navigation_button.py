from kivy.metrics import dp, sp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatIconButton


class NavigationButton(MDRectangleFlatIconButton):
	''' Кнопка, использующаяся в меню навигации '''

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
