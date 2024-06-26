from typing import List
from dataclasses import dataclass

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from data_base import Emergency, Human, Short
from .top_panel import NotebookTopPanelElement
from .contacts import NotebookPhoneContent
from .information import NotebookInfoContent
from .controller import CallController
from ui.widgets.triple_checkbox import FDTripleCheckbox


@dataclass
class NotebookTab:
	''' Хранит данные о вкладке FDNotebook'а '''

	top_panel: NotebookTopPanelElement
	phone_content: NotebookPhoneContent
	info_content: NotebookInfoContent
	emergency: Emergency
	state: bool = False

	def __post_init__(self):
		self._controller = CallController(self.emergency)

		# Add callback for TripleCheckbox
		for triple_checkbox in self.phone_content.children:
			if isinstance(triple_checkbox, FDTripleCheckbox):
				human = Human.query.filter_by(title=triple_checkbox.title).first()
				triple_checkbox.ids.checkbox.bind(on_release=lambda *_, h=human: self._call_human_and_update_logs(h))

		# Adding short text by clicked to ShortButton
		for short_btn in self.info_content.ids.shorts_layout.children:
			short = short_btn.short
			short_btn.bind(on_release=lambda *_, s=short: self._add_short_and_update_logs(s))

		# Adding text from information text
		text_field = self.info_content.ids.addition_info_field
		text_field.bind(text=lambda *_: self._update_info_text_and_logs(text_field))

		self._update_logs()

	def _call_human_and_update_logs(self, human: Human) -> None:
		'''
		Вызвать метод контроллера вызова Человека и обновить логи.

		~params:
		human: Human - запись из БД с информацией о Человеке.
		'''

		self._controller.call_human(human)
		self._update_logs()

	def _add_short_and_update_logs(self, short: Short) -> None:
		'''
		Вызвать метод контроллера добавления Сокращения и обновить логи.

		~params:
		short: Short - запись из БД с информацией о Сокращении.
		'''

		self._controller.add_short(short)
		self._update_logs()

	def _update_info_text_and_logs(self, text_field: MDLabel) -> None:
		'''
		Обновить текст логов из "Дополнительная информация" и обновить логи.

		~params:
		text_field: MDLabel - текстовое поле с "Дополнительной информацией".
		'''

		# self._controller.update_info_text(text_field)
		self._update_logs()

	def _update_logs(self) -> None:
		''' Обновить текстовое поле с логами выезда '''

		self.info_content.logs_label.text = str(self)

	def __str__(self):
		return str(self._controller)


class NotebookManager:
	''' Управляет табами '''

	def __init__(self, tab_panel: MDBoxLayout, phone_content: MDBoxLayout, info_content: MDBoxLayout):
		self.tab_panel = tab_panel
		self.phone_content = phone_content
		self.info_content = info_content

		self.tabs: List[NotebookTab] = []
		self.current_tab = 0

	def add_tab(self, emergency: Emergency) -> NotebookTab:
		'''
		Добавляет вкладку.

		~params:
		emergency: Emergency - запись из БД о выезде.
		'''

		# Init Notebook tab layouts
		top_panel = NotebookTopPanelElement(title=emergency.title)
		phone_content = NotebookPhoneContent(
			description=emergency.description,
			humans=emergency.humans
		)
		info_content = NotebookInfoContent()
		info_content.fill_shorts(emergency.shorts)

		new_tab = NotebookTab(
			top_panel=top_panel,
			phone_content=phone_content,
			info_content=info_content,
			emergency=emergency
		)
		self.tabs.append(new_tab)

		# Bind Notebook tag components
		new_tab.top_panel.bind_open(lambda: self.show_tab(new_tab))
		new_tab.top_panel.bind_close(lambda: self.close_tab(new_tab))

		return new_tab

	def show_tab(self, tab: NotebookTab) -> None:
		'''
		Отображает переданную вкладку.

		~params:
		tab: NotebookTab - вкладка для отображения.
		'''

		for tab_ in self.tabs:
			self.phone_content.remove_widget(tab_.phone_content)
			self.info_content.remove_widget(tab_.info_content)
			tab_.state = False

		self.phone_content.add_widget(tab.phone_content)
		self.info_content.add_widget(tab.info_content)
		tab.state = True

	def close_tab(self, tab: NotebookTab) -> None:
		'''
		Закрывает переданную вкладку.

		~params:
		tab: NotebookTab - вкладка, которая будет закрыта.
		'''

		for index, tab_ in enumerate(self.tabs):
			if tab is tab_:
				self.tab_panel.remove_widget(tab.top_panel)
				self.phone_content.remove_widget(tab.phone_content)
				self.info_content.remove_widget(tab.info_content)

				del self.tabs[index]
				break

		if len(self.tabs) > 0:
			self.show_tab(self.tabs[index-1])
