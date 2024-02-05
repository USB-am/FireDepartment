from typing import List
from dataclasses import dataclass

from kivymd.uix.boxlayout import MDBoxLayout

from data_base import Emergency
from .top_panel import NotebookTopPanelElement
from .contacts import NotebookPhoneContent
from .information import NotebookInfoContent


@dataclass
class NotebookTab:
	''' Хранит данные о вкладке FDNotebook'а '''

	top_panel: NotebookTopPanelElement
	phone_content: NotebookPhoneContent
	info_content: NotebookInfoContent
	state: bool = False


class NotebookManager:
	''' Управляет табами '''

	def __init__(self, tab_panel: MDBoxLayout, phone_content: MDBoxLayout, info_content: MDBoxLayout):
		self.tab_panel = tab_panel
		self.phone_content = phone_content
		self.info_content = info_content

		self.tabs: List[NotebookTab] = []
		self.current_tab = 0

	def add_tab(self, emergency: Emergency) -> NotebookTab:
		'''
		Добавляет вкладку.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		# Init Notebook tab layouts
		top_panel = NotebookTopPanelElement(title=emergency.title)
		phone_content = NotebookPhoneContent(
			description=emergency.description,
			humans=emergency.humans
		)
		info_content = NotebookInfoContent()
		info_content.fill_shorts(emergency.shorts)

		new_tab = NotebookTab(
			top_panel=top_panel,
			phone_content=phone_content,
			info_content=info_content
		)
		self.tabs.append(new_tab)

		# Bind Notebook tag components
		new_tab.top_panel.bind_open(lambda: self.show_tab(new_tab))
		new_tab.top_panel.bind_close(lambda: self.close_tab(new_tab))

		return new_tab

	def show_tab(self, tab: NotebookTab) -> None:
		'''
		Отображает переданную вкладку.

		~params:
		tab: NotebookTab - вкладка для отображения.
		'''

		for tab_ in self.tabs:
			self.phone_content.remove_widget(tab_.phone_content)
			self.info_content.remove_widget(tab_.info_content)
			tab_.state = False

		self.phone_content.add_widget(tab.phone_content)
		self.info_content.add_widget(tab.info_content)
		tab.state = True

	def close_tab(self, tab: NotebookTab) -> None:
		'''
		Закрывает переданную вкладку.

		~params:
		tab: NotebookTab - вкладка, которая будет закрыта.
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
