from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from dataclasses import dataclass

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
class DBEntry:
	title: str
	description: str
	urgent: bool
	tags: list
	humans: list


class TopPanelTab(MDBoxLayout):
	''' Вкладка '''

	title = StringProperty()


class TopPanel(MDBoxLayout):
	''' Поле для отображения  вкладок '''

	def add_tab(self, tab: TopPanelTab) -> None:
		container = self.ids.tabs_container
		container.add_widget(tab)


class TabContent(MDBoxLayout):
	''' Содержимое ячейки '''

	def __init__(self, db_entry):
		super().__init__()

		self.db_entry = db_entry


class Page:
	def __init__(self, emergency: DBEntry):
		self.emergency = emergency

		self.top_tab = TopPanelTab(title=emergency.title)
		self.content = TabContent(db_entry=emergency)


class FDNotebook(MDBoxLayout):
	''' Виджет Notebook '''

	def add_page(self, entry: DBEntry):
		new_page = Page(entry)
		self.ids.top_panel.add_tab(new_page.top_tab)
		self.ids.text_content.text = entry.title


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
				humans=[f'Human #{i+1}' for i in range(10)]
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