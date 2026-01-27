from typing import Callable

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

from config import MAIN_SCREEN_LAYOUTS, ICONS


Builder.load_file(MAIN_SCREEN_LAYOUTS)


class MainScreenInfoElement(MDBoxLayout):
	'''
	Информационный элемент списка на главной странице.
	'''

	def __init__(self, title: str, description: str, **options):
		self.title = title
		self.description = description
		super().__init__(**options)


class MainScreenListElement(MDCard):
	''' Элемент списка на Главной странице '''

	def __init__(self, emergency: 'Emergency', **options):
		self.emergency = emergency
		self.text = emergency.title
		self.icon = ICONS['urgent'][emergency.urgent]
		super().__init__(**options)

	def update(self) -> None:
		pass

	def bind_open_button(self, *args, **kwargs):
		pass
