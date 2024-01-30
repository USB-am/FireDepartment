import datetime
from dataclasses import dataclass
from typing import List, Callable, Optional

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from data_base import db, Emergency, Human, Short, Rank
from config import NOTEBOOK_WIDGET
from ui.widgets.triple_checkbox import FDTripleCheckbox
from ui.field.short import FDShortField


Builder.load_file(NOTEBOOK_WIDGET)


def get_explanation_text(short: Short) -> str:
	'''
	Возвращает форматированный текст из short'a.
	[explanation text format's]:
	- daytime
	- timeday
	- time
	- day

	~params:
	short: Short - запись модели Short.
	'''

	if short.explanation is None:
		return short.title

	now_datetime = datetime.datetime.now()
	returnable_explanation = short.explanation.format(
		daytime=now_datetime.strftime('%d.%m.%Y %H:%M'),
		timeday=now_datetime.strftime('%H:%M %d.%m.%Y'),
		time=now_datetime.strftime('%H:%M'),
		day=now_datetime.strftime('%d.%m.%Y'),
	)

	return f'{returnable_explanation}\n'


class NotebookLog:
	''' Представление лога '''

	def __init__(self, text: str):
		self.text = text
		self.create_time = datetime.datetime.now()

	def __str__(self):
		str_datetime = self.create_time.strftime('%H:%S %d.%m.%Y')
		return f'[{str_datetime}] {self.text}'


class NotebookInformationText(MDLabel):
	''' Область для отображения логов вызова '''

	def __init__(self, **options):
		self.logs: List[NotebookLog] = [NotebookLog('Начало выезда'),]
		super().__init__(**options)

	def add_phone_log(self, entry: Human, status: int) -> None:
		'''
		Добавить в историю событие звонка/попытки связи с сотрудником.

		~params:
		entry: Human - запись о сотруднике;
		status: int - статус события:
			0 - не было звонка;
			1 - успешный звонок;
			2 - неуспешный звонок.
		'''

		pass

	def __str__(self):
		return ''.join(map(str, self.logs))


class NotebookTopPanelElement(MDBoxLayout):
	''' Таб верхней панели FDNotebook'а '''

	title = StringProperty()

	def bind_open(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки открытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.tab_title.bind(on_release=lambda *_: callback())

	def bind_close(self, callback: Callable) -> None:
		'''
		Привязывает событие к нажатию кнопки закрытия.

		~params:
		callback: Callable - событие, которое будет вызываться при нажатии.
		'''

		self.ids.close_btn.bind(on_release=lambda *_: callback())


class NotebookPhoneContent(MDBoxLayout):
	'''
	Содержимое вкладки с контактами.

	~params:
	humans: List[Human] - список людей, участвующих в выезде.
	'''

	def __init__(self, description: str, humans: List[Human], **options):
		self.description = description
		self.humans = humans
		self.checkboxes: List[FDTripleCheckbox] = []

		super().__init__(**options)

		humans_with_rank = filter(
			lambda h: bool(h.rank),
			self.humans)
		sorted_by_rank = sorted(
			humans_with_rank,
			key=lambda h: Rank.query.get(h.rank).priority,
			reverse=True)

		for human in sorted_by_rank:
			checkbox = FDTripleCheckbox(
				normal_icon='phone',
				active_icon='phone-check',
				deactive_icon='phone-cancel',
				title=human.title,
				substring=human.phone_1 if human.phone_1 is not None else ''
			)
			self.checkboxes.append(checkbox)
			self.add_widget(checkbox)


class NotebookInfoContent(MDBoxLayout):
	''' Содержимое вкладки с информацией '''

	def __init__(self, **options):
		super().__init__(**options)

		self.manager = NotebookInformationText()
		self.add_widget(self.manager)

	def fill_shorts(self, shorts: List[Short]) -> None:
		''' Отобразить хоткеи '''

		layout = self.ids.shorts_layout

		for short in shorts:
			short_btn = FDShortField(short)
			short_btn.bind(on_release=lambda *_, s=short: self.insert_info_text(s))
			layout.add_widget(short_btn)

	def insert_info_text(self, short: Short) -> None:
		''' Вставить текст в поле информации '''

		text_area = self.ids.addition_info_field
		inserted_text = get_explanation_text(short)

		text_area.insert_text(inserted_text, from_undo=False)


@dataclass
class _NotebookTab:
	''' Хранит данные о вкладке FDNotebook'а '''

	top_panel: NotebookTopPanelElement
	phone_content: NotebookPhoneContent
	info_content: NotebookInfoContent
	state: bool = False


class _NotebookManager:
	''' Управляет табами '''

	def __init__(self, tab_panel: MDBoxLayout, phone_content: MDBoxLayout, info_content: MDBoxLayout):
		self.tab_panel = tab_panel
		self.phone_content = phone_content
		self.info_content = info_content

		self.tabs: List[_NotebookTab] = []
		self.current_tab = 0

	def add_tab(self, emergency: Emergency) -> _NotebookTab:
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

		new_tab = _NotebookTab(
			top_panel=top_panel,
			phone_content=phone_content,
			info_content=info_content
		)
		self.tabs.append(new_tab)

		# Bind Notebook tag components
		new_tab.top_panel.bind_open(lambda: self.show_tab(new_tab))
		new_tab.top_panel.bind_close(lambda: self.close_tab(new_tab))

		for checkbox in new_tab.phone_content.checkboxes:
			# checkbox.ids.checkbox.bind(on_release=lambda )
			pass

		return new_tab

	def show_tab(self, tab: _NotebookTab) -> None:
		'''
		Отображает переданную вкладку.

		~params:
		tab: _NotebookTab - вкладка для отображения.
		'''

		for tab_ in self.tabs:
			self.phone_content.remove_widget(tab_.phone_content)
			self.info_content.remove_widget(tab_.info_content)
			tab_.state = False

		self.phone_content.add_widget(tab.phone_content)
		self.info_content.add_widget(tab.info_content)
		tab.state = True

	def close_tab(self, tab: _NotebookTab) -> None:
		'''
		Закрывает переданную вкладку.

		~params:
		tab: _NotebookTab - вкладка, которая будет закрыта.
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


class FDNotebook(MDBoxLayout):
	''' Виджет с табами '''

	def __init__(self, **options):
		super().__init__(**options)

		self._manager = _NotebookManager(
			tab_panel=self.ids.tab_panel,
			phone_content=self.ids.phone_content,
			info_content=self.ids.info_content
		)

	def add_tab(self, emergency: Emergency) -> None:
		new_tab = self._manager.add_tab(emergency)

		self.ids.tab_panel.add_widget(new_tab.top_panel)

		self._manager.show_tab(new_tab)

	def get_current_tab(self) -> Optional[_NotebookTab]:
		''' Возвращает текущую вкладку. '''

		if len(self._manager.tabs) == 0:
			return None

		for tab in self._manager.tabs:
			if tab.state:
				return tab
