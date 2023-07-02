from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from dataclasses import dataclass
from typing import Union, List

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_file('tabs.kv')


@dataclass
class FDTripleCheckbox:
	''' Имитация тройного чекбокса '''
	title: str
	substring: str
	state: int


@dataclass
class Firefigher:
	title: str
	phone_1: str
	phone_2: str


@dataclass
class DBEntry:
	title: str
	description: str
	urgent: bool
	tags: list
	humans: List[Firefigher]


class TopPanelTab(MDBoxLayout):
	''' Вкладка '''

	title = StringProperty()

	def bind_open_event(self, callback) -> None:
		self.ids.open_btn.bind(on_release=callback)


class TopPanel(MDBoxLayout):
	''' Поле для отображения  вкладок '''

	def add_tab(self, tab: TopPanelTab) -> None:
		container = self.ids.tabs_container
		container.add_widget(tab)


class TabContent:
	''' Содержимое ячейки '''

	def __init__(self, db_entry: DBEntry):
		self.db_entry = db_entry

		self.title = db_entry.title
		self.description = db_entry.description
		self.firefighers = db_entry.humans
		self.tags = db_entry.tags

		self.triple_checkbox = [FDTripleCheckbox(
		                        title=firefigher.title,
		                        substring=firefigher.phone_1 if firefigher.phone_1 is not None else '',
		                        state=0
			)
			for firefigher in self.firefighers
		]


class Page:
	last_id = 0

	def __new__(cls, *args, **kwargs):
		Page.last_id += 1

		return object.__new__(cls)

	def __init__(self, emergency: DBEntry):
		self.id = self.last_id
		self.emergency = emergency

		self.top_tab = TopPanelTab(title=emergency.title)
		self.content = TabContent(db_entry=emergency)

		self.top_tab.bind_open_event(
			lambda e: print(f'Open "{self.top_tab.title}" tab event')
		)


class FDNotebook(MDBoxLayout):
	''' Виджет Notebook '''

	def __init__(self):
		super().__init__()

		self.pages = []

	def add_page(self, entry: DBEntry):
		new_page = Page(entry)
		self.ids.top_panel.add_tab(new_page.top_tab)
		self.ids.text_content.text = entry.title

		self.pages.append(new_page)


class TestScreen(Screen):
	def __init__(self):
		super().__init__()

		notebook = FDNotebook()
		self.add_widget(notebook)

		for j in range(10):
			entry = DBEntry(
				title=f'Title #{j+1}',
				description='Description',
				urgent=True,
				tags=[f'Tag #{i+1}' for i in range(10)],
				humans=[Firefigher(
						title=f'Human #{i+1}',
						phone_1=f'8 800 555 35 3{i}',
						phone_2=''
					)
				for i in range(10)]
			)
			notebook.add_page(entry)


class MyApp(MDApp):
	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(TestScreen())

	def build(self):
		return self.screen_manager


if __name__ == '__main__':
	MyApp().run()