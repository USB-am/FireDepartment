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


def is_work_day(work_day: date, worktype: Worktype) -> bool:
	'''
	Возвращает True, если work_day является рабочим днем по графику worktype.

	~params:
	work_day: date - дата проверки;
	worktype: Worktype - запись из БД о графике работы.
	'''

	work_week_length = worktype.work_day_range + worktype.week_day_range
	work_length = worktype.finish_work_day - worktype.start_work_day

	return not work_day.day % 4


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
		self.month_title = MONTHS[self.now_date.month]

		self.days: List[FDCalendarDay] = []

		super().__init__(**options)

		self._update_days()
		self._fill_work_days()

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
		work_day = datetime.now().date()
		worktype_id = 1

		if None in (work_day, worktype_id):
			return

		worktype = Worktype.query.get(worktype_id)
		for day in self.days:
			if is_work_day(day.date, worktype):
				day.md_bg_color = (1, 0, 0, .3)
