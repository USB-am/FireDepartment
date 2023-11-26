from dataclasses import dataclass
from typing import Callable, List

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty

from data_base import Emergency, Human
from config import NOTEBOOK_WIDGET
from ui.widgets.triple_checkbox import FDTripleCheckbox


Builder.load_file(NOTEBOOK_WIDGET)


class NotebookTopPanelElement(MDBoxLayout):
	''' Таб верхней панели FDNotebook'а '''

	title = StringProperty()


class NotebookPhoneContent(MDBoxLayout):
	'''
	Содержимое вкладки с контактами.

	~params:
	humans: list[Human] - список людей, участвующих в выезде.
	'''

	def __init__(self, humans: List[Human], **options):
		self.humans = humans
		self.checkboxes: List[FDTripleCheckbox] = []

		super().__init__(**options)

		for human in self.humans:
			checkbox = FDTripleCheckbox(
				normal_icon='phone',
				active_icon='phone-check',
				deactive_icon='phone-cancel',
				title=human.title,
				substring=human.phone_1
			)
			self.checkboxes.append(checkbox)
			self.add_widget(checkbox)


class NotebookInfoContent(MDBoxLayout):
	''' Содержимое вкладки с информацией '''


@dataclass
class _NotebookTab:
	''' Хранит данные о вкладке FDNotebook'а '''

	top_panel: NotebookTopPanelElement
	phone_content: NotebookPhoneContent
	info_content: NotebookInfoContent


class _NotebookManager:
	''' Управляет табами '''

	def __init__(self):
		self.tabs: list[_NotebookTab] = []

	def add_tab(self, emergency: Emergency) -> _NotebookTab:
		'''
		Добавляет вкладку.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		top_panel = NotebookTopPanelElement(title=emergency.title)
		phone_content = NotebookPhoneContent(humans=emergency.humans)
		info_content = NotebookInfoContent()

		new_tab = _NotebookTab(
			top_panel=top_panel,
			phone_content=phone_content,
			info_content=info_content
		)
		self.tabs.append(new_tab)

		return new_tab


class FDNotebook(MDBoxLayout):
	''' Виджет с табами '''

	def __init__(self, **options):
		super().__init__(**options)

		self._manager = _NotebookManager()

	def add_tab(self, emergency: Emergency) -> None:
		new_tab = self._manager.add_tab(emergency)

		self.ids.tab_panel.add_widget(new_tab.top_panel)
