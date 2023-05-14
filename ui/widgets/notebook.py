from kivy.lang.builder import Builder
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

		new_tab = FDTab(self, entry)
		self.tabs.append(new_tab)
		self.ids.top_bar.add_widget(new_tab.top_bar_tab)

		self.move_to_tab(new_tab)

	def move_to_tab(self, tab) -> None:
		''' Собитие перехода на вкладку '''
		self.clear_content()

		self.update_tabs_top_bg(tab)

	def update_tabs_top_bg(self, active_tab) -> None:
		''' Обновление заднего фона вкладки '''

		for tab in self.tabs:
			if active_tab is tab:
				active_tab.top_bar_tab.active = True
				break
			tab.top_bar_tab.active = False

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
		self.top_bar_tab.move_bind(callback=self.fill_content)
		# self.fill_content()

	def fill_content(self) -> None:
		''' Заполняет содержимое контентом '''
		self.parent.clear_content()

		description = self.entry.description
		if description is None:
			description = ''

		self.parent.ids.description_content.text = description

		for firefigher in self.entry.humans:
			phone_1 = firefigher.phone_1
			if phone_1 is None:
				phone_1 = ''

			triple_checkbox = FDTripleCheckbox(
				title=firefigher.title,
				substring=phone_1
			)
			self.parent.ids.contacts_container.add_widget(triple_checkbox)


class FDTopBarTab(MDBoxLayout):
	''' Ячейка в верхней прокручиваемой панели '''

	def __init__(self, title: str):
		self.title = title
		self._active = False
		self._callback = lambda: print('Not callback')

		super().__init__()

	@property
	def active(self) -> bool:
		return self._active

	@active.setter
	def active(self, value: bool) -> None:
		if value:
			self.md_bg_color = (0, 0, 0, .05)
		else:
			self.md_bg_color = (0, 0, 0, 0)

		self._active = value

	def move_bind(self, callback) -> None:
		self._callback = callback


class FDTabContent(MDBoxLayout):
	''' Содержимое ячейки '''