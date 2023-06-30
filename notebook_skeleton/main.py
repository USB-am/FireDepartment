from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '650')


from dataclasses import dataclass

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_file('tabs.kv')


class FDTripleCheckbox:
	''' Имитация тройного чекбокса '''

	def __init__(self, title: str, substring: str, state: int):
		self.title = title
		self.substring = substring
		self.state = state


class NoteBookTopPanel(MDBoxLayout):
	''' Верхняя область с вкладками '''


class NoteBookContent(MDBoxLayout):
	''' Содержимое вкладки '''


class FDNoteBook(MDBoxLayout):
	''' Notebook widget '''

	def __init__(self, **options):
		super().__init__(**options)

		self.tabs = []

	def add_tab(self):
		pass


@dataclass
class DBEntry:
	title: str
	description: str
	urgent: bool
	tags: list
	humans: list


class TopPanelTab(MDBoxLayout):
	''' Вкладка '''

	def __init__(self, title: str):
		super().__init__()

		self.title = title


class FDTab:
	def __init__(self, entry: DBEntry):
		self.entry = entry

		self.top_panel_tab = TopPanelTab(entry.title)
		self.firefighter_list = self._init_firefighter_list()

	def _init_firefighter_list(self) -> list:
		firefighter_list = []

		for human in self.entry.humans:
			list_element = FDTripleCheckbox(
				title=human.title,
				substring=human.phone_1,
				state=0
			)
			firefighter_list.append(list_element)

	def get_content(self) -> dict:
		''' Возвращает информацию для заполнения контента '''

		return {
			'title': self.entry.title,
			'description': self.entry.description,
			'firefighters': self.firefighter_list,
		}

	def __str__(self):
		return f'<FDTab \'{self.entry.title}\'>'


class TestScreen(Screen):
	def __init__(self):
		super().__init__()

		self.notebook = FDNoteBook()
		self.add_widget(self.notebook)


class MyApp(MDApp):
	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(TestScreen())

	def build(self):
		return self.screen_manager


if __name__ == '__main__':
	MyApp().run()