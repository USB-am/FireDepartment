from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET
from data_base import Emergency
from ui.fields.switch import FDTripleCheckbox


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

		new_tab = FDTab(self, entry)
		self.ids.top_bar.add_widget(new_tab.top_bar_tab)

	def clear_content(self) -> None:
		''' Очищает содержимое вкладки '''

		self.ids.description_content.text = ''


class FDTab:
	''' Представление вкладки '''

	def __init__(self, parent: FDNotebook, entry: Emergency):
		self.parent = parent
		self.entry = entry

		self.top_bar_tab = FDTopBarTab(title=entry.title)
		self.fill_content()

	def fill_content(self) -> None:
		''' Заполняет содержимое контентом '''

		self.parent.ids.description_content.text = self.entry.description

		for firefigher in self.entry.humans:
			triple_checkbox = FDTripleCheckbox(
				title=firefigher.title,
				substring=firefigher.phone_1
			)
			self.parent.ids.contacts_container.add_widget(triple_checkbox)


class FDTopBarTab(MDBoxLayout):
	''' Ячейка в верхней прокручиваемой панели '''

	title = StringProperty()


class FDTabContent(MDBoxLayout):
	''' Содержимое ячейки '''