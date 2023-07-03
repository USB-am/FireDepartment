from dataclasses import dataclass
from datetime import datetime
from typing import Union, Callable

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET
from data_base import Emergency
from ui.fields.switch import FDTripleCheckbox


Builder.load_file(NOTEBOOK_WIDGET)


class TopPanelTab(MDBoxLayout):
	''' Вкладка '''

	title = StringProperty()

	def bind_open_event(self, callback: Callable) -> None:
		self.ids.open_btn.bind(on_release=callback)


class TopPanel(MDBoxLayout):
	''' Поле для отображения  вкладок '''

	def add_tab(self, tab: TopPanelTab) -> None:
		container = self.ids.tabs_container
		container.add_widget(tab)


class TabContent:
	''' Содержимое ячейки '''

	def __init__(self, db_entry: Emergency):
		self.db_entry = db_entry

		self.title = db_entry.title
		self.description = db_entry.description
		self.firefighers = db_entry.humans
		self.tags = db_entry.tags

		self.triple_checkboxes = [FDTripleCheckbox(
		                        title=firefigher.title,
		                        substring=firefigher.phone_1 if firefigher.phone_1 is not None else '',
		                        state=0
			)
			for firefigher in self.firefighers
		]

	def get_data(self) -> dict:
		data = {
			'title': self.db_entry.title,
			'description': self.db_entry.description,
			'subcontent': self.triple_checkboxes,
			'tags': self.db_entry.tags,
		}

		return data


class Page:
	last_id = 0

	def __new__(cls, *args, **kwargs):
		Page.last_id += 1

		return object.__new__(cls)

	def __init__(self, emergency: Emergency, update_content_callable: Callable):
		self.id = self.last_id
		self.emergency = emergency
		self.update_content_callable = update_content_callable

		self.top_tab = TopPanelTab(title=emergency.title)
		self.content = TabContent(db_entry=emergency)

		self.top_tab.bind_open_event(
			lambda e: self.update_content_callable(self.content.get_data())
		)


class FDNotebook(MDBoxLayout):
	''' Виджет Notebook '''

	def __init__(self):
		super().__init__()

		self.pages = []

	def add_page(self, entry: Emergency):
		new_page = Page(entry, self.update_content)
		self.ids.top_panel.add_tab(new_page.top_tab)

		self.pages.append(new_page)
		self.update_content(new_page.content.get_data())

	def update_content(self, data: dict) -> None:
		self.ids.content_title.text = data['title']
		self.ids.content_description.text = data['description']
		self.ids.addition_information.text = data['title']

		self.ids.subcontent.clear_widgets()

		for element in data['subcontent']:
			self.ids.subcontent.add_widget(element)