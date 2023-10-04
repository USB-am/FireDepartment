from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __FIELD_SWITCH


Builder.load_file(__FIELD_SWITCH)


class FDSwitch(MDBoxLayout):
	''' Виджет с переключателем '''

	icon = StringProperty()
	title = StringProperty()