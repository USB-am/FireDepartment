from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout

from config import MAIN_SCREEN_LAYOUTS
from data_base import Tag, Short, Human, Emergency


Builder.load_file(MAIN_SCREEN_LAYOUTS)


class _ListElementIcon(MDBoxLayout):
	''' Иконка в выпадающей области. '''

	icon = StringProperty()
	value = StringProperty('')


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

		self.ids.info_icons.add_widget(_ListElementIcon(
			icon=Tag.icon,
			value=str(len(self.emergency.tags))
		))
		self.ids.info_icons.add_widget(_ListElementIcon(
			icon=Human.icon,
			value=str(len(self.emergency.humans))
		))
		self.ids.info_icons.add_widget(_ListElementIcon(
			icon=Short.icon,
			value=str(len(self.emergency.shorts))
		))

		if self.emergency.urgent:
			self.ids.info_icons.add_widget(_ListElementIcon(icon='truck-fast'))


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

	def bind_open_button(self, callback: Callable) -> None:
		'''
		Привязка события к кнопке.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.content.ids.open_button.bind(on_release=lambda *_: callback())
