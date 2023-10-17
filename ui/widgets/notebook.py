from kivy.lang.builder import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __WIDGET_NOTEBOOK


Builder.load_file(__WIDGET_NOTEBOOK)


class _FDTabWidget(MDBoxLayout):
	''' Вкладка '''

	title = StringProperty()


class FDTab:
	def __init__(self, title: str, content_cls: MDBoxLayout):
		self.title = title
		self.content_cls = content_cls

		self._tab_widget = _FDTabWidget(title=self.title)


class FDNotebook(MDBoxLayout):
	''' Виджет с вкладками '''

	def __init__(self, **options):
		super().__init__(**options)

		self._tabs = []
		self.add_tab(title='Test #1', content=MDBoxLayout())

	def add_tab(self, title: str, content: MDBoxLayout) -> None:
		new_tab = FDTab(title=title, content_cls=content)
		self._tabs.append(new_tab)

		self.ids.navigation.add_widget(new_tab._tab_widget)
