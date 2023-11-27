from dataclasses import dataclass
from typing import List, Callable, Optional

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import Emergency, Human
from config import NOTEBOOK_WIDGET
from ui.widgets.triple_checkbox import FDTripleCheckbox


Builder.load_file(NOTEBOOK_WIDGET)


class NotebookTopPanelElement(MDBoxLayout):
	''' Таб верхней панели FDNotebook'а '''

	title = StringProperty()

	def bind_open(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки открытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.tab_title.bind(on_release=lambda *_: callback())

	def bind_close(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки закрытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.close_btn.bind(on_release=lambda *_: callback())


class NotebookPhoneContent(MDBoxLayout):
	'''
	Содержимое вкладки с контактами.

	~params:
	humans: List[Human] - список людей, участвующих в выезде.
	'''

	def __init__(self, description: str, humans: List[Human], **options):
		self.description = description
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
	state: bool = False


class _NotebookManager:
	''' Управляет табами '''

	def __init__(self, tab_panel: MDBoxLayout, phone_content: MDBoxLayout, info_content: MDBoxLayout):
		self.tab_panel = tab_panel
		self.phone_content = phone_content
		self.info_content = info_content

		self.tabs: List[_NotebookTab] = []
		self.current_tab = 0

	def add_tab(self, emergency: Emergency) -> _NotebookTab:
		'''
		Добавляет вкладку.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		top_panel = NotebookTopPanelElement(title=emergency.title)
		phone_content = NotebookPhoneContent(
			description=emergency.description,
			humans=emergency.humans
		)
		info_content = NotebookInfoContent()

		new_tab = _NotebookTab(
			top_panel=top_panel,
			phone_content=phone_content,
			info_content=info_content
		)
		self.tabs.append(new_tab)
		new_tab.top_panel.bind_open(lambda: self.show_tab(new_tab))
		new_tab.top_panel.bind_close(lambda: self.close_tab(new_tab))

		return new_tab

	def show_tab(self, tab: _NotebookTab) -> None:
		'''
		Отображает переданную вкладку.

		~params:
		tab: _NotebookTab - вкладка для отображения.
		'''

		for tab_ in self.tabs:
			self.phone_content.remove_widget(tab_.phone_content)
			self.info_content.remove_widget(tab_.info_content)
			tab_.state = False

		self.phone_content.add_widget(tab.phone_content)
		self.info_content.add_widget(tab.info_content)
		tab.state = True

	def close_tab(self, tab: _NotebookTab) -> None:
		'''
		Закрывает переданную вкладку.

		~params:
		tab: _NotebookTab - вкладка, которая будет закрыта.
		'''

		for index, tab_ in enumerate(self.tabs):
			if tab is tab_:
				self.tab_panel.remove_widget(tab.top_panel)
				self.phone_content.remove_widget(tab.phone_content)
				self.info_content.remove_widget(tab.info_content)

				del self.tabs[index]
				break

		if len(self.tabs) > 0:
			self.show_tab(self.tabs[index-1])


class FDNotebook(MDBoxLayout):
	''' Виджет с табами '''

	def __init__(self, **options):
		super().__init__(**options)

		self._manager = _NotebookManager(
			tab_panel=self.ids.tab_panel,
			phone_content=self.ids.phone_content,
			info_content=self.ids.info_content
		)

	def add_tab(self, emergency: Emergency) -> None:
		new_tab = self._manager.add_tab(emergency)

		self.ids.tab_panel.add_widget(new_tab.top_panel)

		self._manager.show_tab(new_tab)

	def get_current_tab(self) -> Optional[_NotebookTab]:
		''' Возвращает текущую вкладку. '''

		if len(self._manager.tabs) == 0:
			return

		for tab in self._manager.tabs:
			if tab.state:
				return tab
