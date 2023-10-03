from kivy.lang.builder import Builder
from kivy.properties import StringProperty

from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __FIELD_INPUT_DIR


Builder.load_file(__FIELD_INPUT_DIR)


class FDInput(MDBoxLayout):
	''' Базовое поле ввода '''

	hint_text = StringProperty()
	help_text = StringProperty('')


class FDLeftIconInput(MDBoxLayout):
	''' Поле ввода с иконкой слева '''

	icon = StringProperty()
	hint_text = StringProperty()
	help_text = StringProperty('')


class FDRightIconInput(MDBoxLayout):
	''' Поле ввода с иконкой справа '''

	icon = StringProperty()
	hint_text = StringProperty()
	help_text = StringProperty('')