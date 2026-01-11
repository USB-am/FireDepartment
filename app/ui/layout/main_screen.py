from typing import Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.boxlayout import MDBoxLayout

from config import MAIN_SCREEN_LAYOUTS, ICONS
# from data_base import Tag, Short, Human, Emergency


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

	def __init__(self, emergency: 'Emergency', **options): # type: ignore
		self.emergency = emergency

		super().__init__(**options)

		self.tags_icon = _ListElementIcon(
			icon=ICONS['Tag'],
			value=str(len(self.emergency.tags)))
		self.ids.info_icons.add_widget(self.tags_icon)

		self.humans_icon = _ListElementIcon(
			icon=ICONS['Human'],
			value=str(len(self.emergency.humans)))
		self.ids.info_icons.add_widget(self.humans_icon)

		self.shorts_icon = _ListElementIcon(
			icon=ICONS['Short'],
			value=str(len(self.emergency.shorts)))
		self.ids.info_icons.add_widget(self.shorts_icon)

		self.is_urgent_icon = _ListElementIcon(
			icon=('', 'truck-fast')[self.emergency.urgent])
		self.ids.info_icons.add_widget(self.is_urgent_icon)

	def update(self) -> None:
		''' Обновить значения тегов, людей и сокращений '''

		self.tags_icon.value = str(len(self.emergency.tags))
		self.humans_icon.value = str(len(self.emergency.humans))
		self.shorts_icon.value = str(len(self.emergency.shorts))
		self.is_urgent_icon.icon = ('', 'truck-fast')[self.emergency.urgent]

		if self.emergency.description is not None:
			self.ids.description_lbl.text = self.emergency.description
		else:
			self.ids.description_lbl.text = ''


class MainScreenListElement(MDExpansionPanel):
	'''
	Элемент списка на главной странице.

	~params:
	emergency: Emergency - запись о выезде из БД;
	**options - дополнительные аргументы для родительского класса.
	'''

	def __init__(self, emergency: 'Emergency', **options): # type: ignore
		self.emergency = emergency
		content = _ListElementContent(emergency)

		options.update({
			'icon': ICONS['Emergency'],
			'content': content,
			'panel_cls': MDExpansionPanelOneLine(
				text=emergency.title
			)
		})

		super().__init__(**options)

	def update(self) -> None:
		''' Обновить отображаемую информацию '''

		self.panel_cls.text = self.emergency.title
		self.content.update()

	def bind_open_button(self, callback: Callable) -> None:
		'''
		Привязка события к кнопке.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.content.ids.open_button.bind(on_release=lambda *_: callback())


class MainScreenInfoElement(MDBoxLayout):
	'''
	Информационный элемент списка на главной странице.
	'''

	def __init__(self, title: str, description: str, **options):
		self.title = title
		self.description = description
		super().__init__(**options)
