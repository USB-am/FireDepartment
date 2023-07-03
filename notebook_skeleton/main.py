from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from dataclasses import dataclass
from typing import Union, List, Callable

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_file('tabs.kv')


class FDTripleCheckbox(MDBoxLayout):
	title = StringProperty()
	substring = StringProperty()
	state = NumericProperty()


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

	def __init__(self, emergency: DBEntry, update_content_callable: Callable):
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

	def add_page(self, entry: DBEntry):
		new_page = Page(entry, self.update_content)
		self.ids.top_panel.add_tab(new_page.top_tab)

		self.pages.append(new_page)
		self.update_content(new_page.content.get_data())

	def update_content(self, data: dict) -> None:
		print(f'FDNotebook.update_content is started')
		self.ids.content_title.text = data['title']
		self.ids.content_description.text = data['description']
		self.ids.addition_information.text = data['title']

		self.ids.subcontent.clear_widgets()

		for element in data['subcontent']:
			self.ids.subcontent.add_widget(element)


class TestScreen(Screen):
	def __init__(self):
		super().__init__()

		notebook = FDNotebook()
		self.add_widget(notebook)

		# Temp fill notebook
		for j in range(10):
			entry = DBEntry(
				title=f'Title #{j+1}',
				description=f'Description for Tab #{j+1}',
				urgent=True,
				tags=[f'Tag #{i+1}' for i in range(10)],
				humans=[Firefigher(
						title=f'Human #{j+1}.{i+1}',
						phone_1=f'8 800 555 3{j} 3{i}',
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