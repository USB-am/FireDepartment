from kivy.lang.builder import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout

from config import MAIN_SCREEN_LAYOUTS
from data_base import Emergency


Builder.load_file(MAIN_SCREEN_LAYOUTS)


class _ListElementContent(MDBoxLayout):
	'''
	Содержимое выпадающей области элемента.

	~params:
	emergency: Emergency - запись о выезде из БД;
	**options - дополнительные аргументы для родительского класса.
	'''

	def __init__(self, emergency: Emergency, **options):
		self.emergency = emergency

		super().__init__(**options)


class MainScreenListElement(MDExpansionPanel):
	'''
	Элемент списка на главной странице.

	~params:
	emergency: Emergency - запись о выезде из БД;
	**options - дополнительные аргументы для родительского класса.
	'''

	def __init__(self, emergency: Emergency, **options):
		self.emergency = emergency

		options.update({
			'icon': Emergency.icon,
			'content': _ListElementContent(emergency),
			'panel_cls': MDExpansionPanelOneLine(
				text=emergency.title
			)
		})

		super().__init__(**options)
