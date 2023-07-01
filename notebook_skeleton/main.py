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


class ContentPanel(MDBoxLayout):
	''' Содержимое ячейки '''


class TestScreen(Screen):
	def __init__(self):
		super().__init__()

		self.notebook = TopPanel()
		self.add_widget(self.notebook)

		for i in range(10):
			tab = TopPanelTab(title=f'Tab #{i}')
			self.notebook.add_tab(tab)


class MyApp(MDApp):
	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(TestScreen())

	def build(self):
		return self.screen_manager


if __name__ == '__main__':
	MyApp().run()