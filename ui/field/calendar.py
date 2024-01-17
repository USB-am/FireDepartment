from typing import List
from datetime import datetime, date, timedelta
from calendar import Calendar

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from data_base import Worktype
from config import CALENDAR_FIELD
from ui.field.date import FDDate
from ui.field.select import FDSelect


Builder.load_file(CALENDAR_FIELD)
CALENDAR = Calendar()
MONTHS = (
	'',
	'Январь',
	'Февраль',
	'Март',
	'Апрель',
	'Май',
	'Июнь',
	'Июль',
	'Август',
	'Сентябрь',
	'Октябрь',
	'Ноябрь',
	'Декабрь',
)


def add_months(current_date: date, months_to_add: int) -> date:
	'''
	Добавить месяц(ы) к current_date.

	~params:
	current_date: date - дата, которая будет увеличена;
	months_to_add: int - количество месяцев, на которое будет увеличено.
	'''

	new_date = date(
		current_date.year + (current_date.month + months_to_add - 1) // 12,
		(current_date.month + months_to_add - 1) % 12 + 1,
		current_date.day
	)

	return new_date


def is_work_day(day: date, work_day: date, worktype: Worktype) -> bool:
	'''
	Возвращает True, если work_day является рабочим днем по графику worktype.

	~params:
	day: date - дата проверки;
	work_day: date - дата начала отсчета;
	worktype: Worktype - запись из БД о графике работы.
	'''

	work_week_length = worktype.work_day_range + worktype.week_day_range
	work_length = worktype.finish_work_day - worktype.start_work_day

	start_work_day_bias = (day - work_day).days
	start_work_week = work_day + timedelta(
		days=start_work_day_bias - (start_work_day_bias % work_week_length)
	)
	finish_work_week = start_work_week + timedelta(days=worktype.work_day_range-1)

	return start_work_week <= day <= finish_work_week


class FDCalendarWeekTitle(MDLabel):
	'''
	Представление дня недели календаря.

	~params:
	text: str - название дня недели.
	'''

	text = StringProperty()


class FDCalendarDay(MDLabel):
	'''
	Представление дня календаря.

	~params:
	date: datetime - представляемый день;
	another_month: bool - указывает, что день относится к другому месяцу.
	'''

	def __init__(self, date: date, another_month: bool=False):
		self.date = date
		if not another_month:
			self.theme_text_color = 'Hint'
		self._is_work_day = False

		super().__init__()

	@property
	def is_work_day(self) -> bool:
		return self._is_work_day

	@is_work_day.setter
	def is_work_day(self, value: bool) -> None:
		'''
		Перезаписывает значение _is_work_day и обновляет заливку.

		~params:
		value: bool - статус дня (рабочий/не рабочий).
		'''

		self._is_work_day = value
		self.md_bg_color = (1, 0, 0, .3) if value else (0, 0, 0, 0)


class FDCalendar(MDBoxLayout):
	'''
	Отображение календаря, отображающего график работы.

	~params:
	from_date_field: FDDate - виджет с датой начала работы;
	worktype_field: FDSelect - виджет с графиками работы.
	'''

	icon = 'calendar-month'

	def __init__(self,
	             from_date_field: FDDate,
	             worktype_field: FDSelect,
	             **options
	            ):
		self.from_date_field = from_date_field
		self.worktype_field = worktype_field

		self.now_date = datetime.now().date()
		self.month_title = '{month}\n{year}'.format(
			month=MONTHS[self.now_date.month],
			year=self.now_date.year
		)

		self.days: List[FDCalendarDay] = []

		super().__init__(**options)

		self.update(self.now_date)

	def _update_days(self, date: date=None) -> None:
		'''
		Обновить страницу календаря на месят, соответствующий date.

		~params:
		date: date - дата, месяц которой будет отображен.
		'''

		if date is not None:
			self.now_date = date

		month_days = CALENDAR.itermonthdates(self.now_date.year, self.now_date.month)
		layout = self.ids.calendar_layout
		layout.clear_widgets()
		self.days = []

		for day in month_days:
			calendar_day = FDCalendarDay(
				date=day,
				another_month=(day.month == self.now_date.month)
			)
			layout.add_widget(calendar_day)
			self.days.append(calendar_day)

	def _fill_work_days(self) -> None:
		''' Выделяет рабочие дни '''

		work_day = self.from_date_field.get_value()
		worktype_id = self.worktype_field.get_value()

		if None in (work_day, worktype_id):
			return

		worktype = Worktype.query.get(worktype_id)
		for day in self.days:
			day.is_work_day = is_work_day(day.date, work_day, worktype)

	def _update_month_title(self, date: date) -> None:
		''' Обновить название месяца '''

		self.month_title = '{month}\n{year}'.format(
			month=MONTHS[date.month],
			year=date.year
		)
		self.ids.month_title_label.text = self.month_title

	def _update_information(self) -> None:
		''' Обновляет область с информацией справа '''

		work_days = list(filter(lambda day: day.is_work_day, self.days))
		now_date = datetime.now().date()
		next_work_days = list(filter(lambda day: day.date >= now_date, work_days))[:2]
		try:
			self.ids.next_work_day_label.text = str(next_work_days[0].date)
		except IndexError:
			pass
		try:
			self.ids.next_next_work_day_label.text = str(next_work_days[1].date)
		except IndexError:
			pass

	def prev_month(self) -> None:
		''' Переключение календаря на месяц назад '''

		self.now_date = add_months(self.now_date, -1)
		self.update(self.now_date)

	def next_month(self) -> None:
		''' Переключение календаря на месяц вперед '''

		self.now_date = add_months(self.now_date, 1)
		self.update(self.now_date)

	def update(self, date: date=None) -> None:
		''' Обновить календарь '''

		print(date)
		if date is None:
			return

		self._update_month_title(date)
		self._update_days(date)
		self._fill_work_days()
		self._update_information()

		self.now_date = date
