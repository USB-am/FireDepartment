from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __TOOLBAR_DIR


Builder.load_file(__TOOLBAR_DIR)


class Toolbar(MDBoxLayout):
	''' Верхняя полоска '''