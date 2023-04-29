from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET
from data_base import Emergency


Builder.load_file(NOTEBOOK_WIDGET)


class FDTopBarTab(MDBoxLayout):
	''' Ячейка в верхней прокручиваемой панели '''

	title = StringProperty()


class FDTabContent(MDBoxLayout):
	''' Содержимое ячейки '''


class FDNotebook(MDBoxLayout):
	''' Виджет с вкладками '''

	def __init__(self):
		super().__init__()

		self.tabs = []

		# Temp
		for emergency in Emergency.query.all()[:3]:
			self.add_tab(emergency)

	def add_tab(self, entry: Emergency) -> None:
		''' Добавляет новую вкладку '''

		top_bar_tab = FDTopBarTab(title=entry.title)
		self.ids.top_bar.add_widget(top_bar_tab)