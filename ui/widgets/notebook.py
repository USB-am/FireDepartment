from dataclasses import dataclass
from datetime import datetime

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
		new_tab.fill_content()

	def close_tab(self, tab) -> None:
		try:
			self.tabs.remove(tab)

			for active_tab in self.ids.top_bar.children:
				if active_tab is tab.top_bar_tab:
					self.ids.top_bar.remove_widget(tab.top_bar_tab)
					break

		except ValueError as error:
			print(error)

	def move_to_tab(self, tab) -> None:
		''' Собитие перехода на вкладку '''
		self.clear_content()

		self.update_tabs_top_bg(tab)

	def update_tabs_top_bg(self, active_tab) -> None:
		''' Обновление заднего фона вкладки '''

		for tab in self.tabs:
			if active_tab is tab:
				active_tab.top_bar_tab.active = True
			else:
				tab.top_bar_tab.active = False

	def clear_content(self) -> None:
		''' Очищает содержимое вкладки '''

		# Clear description
		self.ids.description_content.text = ''

		# Clear contact-humans
		self.ids.contacts_container.clear_widgets()

		# Clear information text
		self.ids.info_entry.text = ''


@dataclass
class Call:
	humans: list
	info: str


@dataclass
class CallHuman:
	name: str
	phone: str
	status: int


class FDTab:
	''' Представление вкладки '''

	def __init__(self, parent: FDNotebook, entry: Emergency):
		self.parent = parent
		self.entry = entry

		self.top_bar_tab = FDTopBarTab(title=entry.title)
		self.top_bar_tab.move_bind(callback=self.fill_content)
		self.top_bar_tab.close_bind(callback=self.close)

		self.record = self.init_info()

	def init_info(self) -> Call:
		humans = []

		for firefigher in self.entry.humans:
			name = firefigher.title
			phone = '' if firefigher.phone_1 is None else firefigher.phone_1
			call_human = CallHuman(name=name, phone=phone, status=0)
			humans.append(call_human)

		info = 'Начало вызова в {}.\n'.format(
			datetime.now().strftime('%d.%m.%Y %H:%M:%S')
		)

		return Call(humans, info)

	def fill_content(self) -> None:
		''' Заполняет содержимое контентом '''

		def update_firefigher_status(firefigher: CallHuman, status: int) -> None:
			firefigher.status = status

		self.parent.clear_content()

		description = self.entry.description
		if description is None:
			description = ''
		self.parent.ids.description_content.text = description

		for firefigher in self.record.humans:
			triple_checkbox = FDTripleCheckbox(
				title=firefigher.name,
				substring=firefigher.phone
			)
			triple_checkbox.set_value(firefigher.status)
			triple_checkbox.ids.icon_btn.bind(
				on_release=lambda e: update_firefigher_status(
					firefigher=firefigher,
					status=triple_checkbox.get_value()
				)
			)
			print(firefigher.status)
			self.parent.ids.contacts_container.add_widget(triple_checkbox)

		self.parent.update_tabs_top_bg(self)

	def close(self) -> None:
		print(f'Close {self.entry.title} tab is pressed')
		self.parent.close_tab(self)


class FDTopBarTab(MDBoxLayout):
	''' Ячейка в верхней прокручиваемой панели '''

	def __init__(self, title: str):
		self.title = title
		self._active = False
		self._callback = lambda: print('Not move event')
		self._close = lambda: print('Not close event')

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

	def close_bind(self, callback) -> None:
		self._close = callback


class FDTabContent(MDBoxLayout):
	''' Содержимое ячейки '''