from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET


Builder.load_file(NOTEBOOK_WIDGET)


class FDNotebook(MDBoxLayout):
	''' Виджет с вкладками '''