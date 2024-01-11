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

	# wt_start = worktype.start_work_day.date()
	wt_start = work_day
	start_work_day_bias = (day - wt_start).days
	start_work_week = wt_start + timedelta(
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
	date: datetime - представляемый день.
	'''

	def __init__(self, date: date, another_month: bool=False):
		self.date = date
		if not another_month:
			self.theme_text_color = 'Hint'

		super().__init__()


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
		work_day = datetime.now().date() + timedelta(days=1)
		worktype_id = 1

		if None in (work_day, worktype_id):
			return

		worktype = Worktype.query.get(worktype_id)
		for day in self.days:
			if is_work_day(day.date, work_day, worktype):
				day.md_bg_color = (1, 0, 0, .3)

	def _update_month_title(self, date: date) -> None:
		''' Обновить название месяца '''

		self.month_title = '{month}\n{year}'.format(
			month=MONTHS[date.month],
			year=date.year
		)
		self.ids.month_title_label.text = self.month_title

	def update(self, date: date) -> None:
		''' Обновить календарь '''

		self._update_month_title(date)
		self._update_days(date)
		self._fill_work_days()
