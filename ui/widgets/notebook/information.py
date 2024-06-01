from typing import List, Callable
from datetime import datetime

from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from data_base import Short, Human
from ui.field.short import FDShortField
from ui.widgets.triple_checkbox import FDTripleCheckbox


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

	now_datetime = datetime.now()
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
		self.create_time = datetime.now()

	def __str__(self):
		str_datetime = self.create_time.strftime('%d.%m.%Y %H:%M')
		return f'[{str_datetime}] {self.text}'


class NotebookInformationText(MDLabel):
	''' Область для отображения логов вызова '''

	def __init__(self, **options):
		self.logs: List[NotebookLog] = [NotebookLog('Начало выезда.'),]
		super().__init__(**options)

	def add_phone_log(self, checkbox: FDTripleCheckbox) -> None:
		'''
		Добавить в историю событие звонка/попытки связи с сотрудником.

		~params:
		checkbox: FDTripleCheckbox - тройной checkbox с информацией о вызове сотруднику.
		'''

		human_name = checkbox.title
		phone = checkbox.substring
		status = (checkbox.state + 1) % 3

		if status == 1:
			log_text = f'Звонок {human_name} на номер {phone}.'
		elif status == 2:
			log_text = f'Звонок {human_name} не прошел.'
		else:
			return

		self.logs.append(NotebookLog(log_text))
		self.update_logs()

	def add_short_log(self, entry: Short) -> None:
		'''
		Добавить в историю событие из Short.

		~params:
		entry: Short - добавляемые данные.
		'''

		short_without_text_transfer = get_explanation_text(entry)[:-1]
		self.logs.append(short_without_text_transfer)
		self.update_logs()

	def update_logs(self) -> None:
		self.text = str(self)

	def __str__(self):
		return '\n'.join(map(str, self.logs[::-1]))


class NotebookInfoContent(MDBoxLayout):
	''' Содержимое вкладки с информацией '''

	def __init__(self, **options):
		super().__init__(**options)

		# self.manager = NotebookInformationText()
		# self.manager.texture_update()
		# self.add_widget(self.manager)

	def fill_shorts(self, shorts: List[Short]) -> None:
		''' Отобразить хоткеи '''

		layout = self.ids.shorts_layout

		for short in shorts:
			short_btn = FDShortField(short)
			short_btn.bind(on_release=lambda *_, s=short: self.insert_info_text(s))
			# short_btn.bind(on_release=lambda *_, s=short: self.manager.add_short_log(s))
			layout.add_widget(short_btn)

	def insert_info_text(self, short: Short) -> None:
		''' Вставить текст в поле информации '''

		text_area = self.ids.addition_info_field
		inserted_text = get_explanation_text(short)

		text_area.insert_text(inserted_text, from_undo=False)
