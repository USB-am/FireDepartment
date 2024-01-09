from typing import List
from datetime import datetime, date, timedelta
from calendar import Calendar

from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from data_base import Worktype
from config import CALENDAR_FIELD


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


def is_work_day(date: date, start_work_day: date, worktype_id: int) -> bool:
	'''
	Проверяет является date рабочим днем по графику worktype, начиная с дня start_work_day.

	~params:
	date: date - дата, которая будет проверяться;
	start_work_day: date - дата начала отсчета;
	worktype_id: int - id записи о графике работы.
	'''

	worktype = Worktype.query.get(worktype_id)
	current_time = datetime.now().time()
	diff_dates = date - start_work_day
	date = datetime(
		date.year,
		date.month,
		date.day,
		current_time.hour,
		current_time.minute,
		current_time.second)
	work_length = worktype.finish_work_day - worktype.start_work_day
	work_week_length = worktype.work_day_range + worktype.week_day_range

	start_day = start_work_day + diff_dates
	start_date = start_day - timedelta(
		days=diff_dates.days % work_week_length
	)
	start_week = datetime(
		year=start_date.year,
		month=start_date.month,
		day=start_date.day,
		hour=worktype.start_work_day.hour,
		minute=worktype.start_work_day.minute)
	finish_week = start_week + work_length

	return start_week <= date <= finish_week


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

	def __init__(self, date: datetime, another_month: bool=False):
		self.date = date
		if not another_month:
			self.theme_text_color = 'Hint'

		super().__init__()


class FDCalendar(MDBoxLayout):
	'''
	Отображение календаря, отображающего график работы.

	~params:
	start_work_day: date - день для начала отсчета;
	worktype: Worktype - запись из БД о графике работы;
	for_date: datetime - месяц, который будет отображен.
	'''

	icon = 'calendar-month'

	def __init__(self,
	             start_work_day: date=None,
	             worktype: Worktype=None,
	             for_date: datetime=datetime.now(),
	             **options
	            ):
		self.start_work_day = start_work_day
		self.worktype = worktype
		self._date = for_date
		self.month_title = MONTHS[self._date.month]

		super().__init__(**options)

		week_days_layout = self.ids.week_days_layout
		for day in ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'):
			week_days_layout.add_widget(FDCalendarWeekTitle(text=day))

		self.update()

	def update(self,
	           start_work_day: datetime=None,
	           worktype: Worktype=None,
	           for_date: datetime=None
	          ) -> None:
		'''
		Производит перерасчет рабочего времени.

		~params:
		start_work_day: date=None - день для начала отсчета;
		worktype: Worktype=None - запись из БД о графике работы.
		'''

		if start_work_day is not None:
			self.start_work_day = start_work_day
		if worktype is not None:
			self.worktype = worktype
		if for_date is not None:
			self._date = for_date

		layout = self.ids.calendar_layout
		layout.clear_widgets()

		month_days = CALENDAR.itermonthdates(self._date.year, self._date.month)

		for date in month_days:
			calendar_day = FDCalendarDay(
				date=date,
				another_month=self._date.month == date.month
			)

			# Rewrite it shit
			if not (None in (self.start_work_day, self.worktype, self._date)):
				if is_work_day(date, self.start_work_day, self.worktype):
					calendar_day.md_bg_color = (1, 0, 0, .3)

			layout.add_widget(calendar_day)
