from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET
from data_base import Emergency


Builder.load_file(NOTEBOOK_WIDGET)


class FDNotebook(MDBoxLayout):
	''' Виджет с вкладками '''

	def __init__(self):
		super().__init__()

		self.tabs = []

		# Temp
		for emergency in Emergency.query.all():
			self.add_tab(emergency)

	def add_tab(self, entry: Emergency) -> None:
		''' Добавляет новую вкладку '''

		new_tab = self._create_tab(entry)

	def _create_tab(self, entry: Emergency):
		''' Создает объект вкладки '''

		return FDTab(self, entry)


class FDTab:
	''' Представление вкладки '''

	def __init__(self, parent: FDNotebook, entry: Emergency):
		self.parent = parent
		self.entry = entry

		self.top_bar_tab = FDTopBarTab(title=entry.title)


class FDTopBarTab(MDBoxLayout):
	''' Ячейка в верхней прокручиваемой панели '''

	title = StringProperty()


class FDTabContent(MDBoxLayout):
	''' Содержимое ячейки '''