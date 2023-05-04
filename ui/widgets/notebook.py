from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import NOTEBOOK_WIDGET
from data_base import Emergency
from ui.fields.switch import FDTripleCheckbox


Builder.load_file(NOTEBOOK_WIDGET)


def split_into_words(text: str, max_length: int) -> str:
	split_text = text.split()

	if not len(split_text):
		return text[:max_length] + '...'

	answer = ''
	for word in split_text:
		if len(answer) + len(word) <= max_length:
			answer += f' {word}'
		else:
			break

	return answer[1:] + '...'


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

		self.clear_content()

		new_tab = FDTab(self, entry)
		self.ids.top_bar.add_widget(new_tab.top_bar_tab)

	def clear_content(self) -> None:
		''' Очищает содержимое вкладки '''

		# Clear description
		self.ids.description_content.text = ''

		# Clear contact-humans
		self.ids.contacts_container.clear_widgets()

		# Clear information text
		self.ids.info_entry.text = ''


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