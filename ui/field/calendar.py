from typing import List, Tuple, Union
from calendar import Calendar
from datetime import datetime, date, timedelta

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from dateutil.relativedelta import relativedelta

from config import CALENDAR_FIELD
from data_base import Worktype, Human
from data_base.manager import get_by_id


Builder.load_file(CALENDAR_FIELD)


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
	new_date = current_date + relativedelta(months=months_to_add)
	return new_date


def is_work_day(day: date, work_day: date, worktype: Worktype) -> bool:
	'''
	Возвращает True, если day является рабочим днем по графику worktype.

	~params:
	day: date - дата проверки;
	work_day: date - дата начала отсчета рабочих дней;
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


def is_working(now_datetime: datetime, human: Human) -> bool:
	'''
	Является ли now_datetime рабочим временем для human.

	~params:
	now_datetime: datetime - время, от которого будет идти проверка;
	human: Human - человек, который будет проверяться.
	'''

	if human.is_vacation:
		return False

	worktype = get_by_id(Worktype, human.worktype)
	work_day = human.work_day
	day = now_datetime.date()

	if not is_work_day(day, work_day, worktype):
		return False

	work_duration = worktype.finish_work_day - worktype.start_work_day
	start_work = datetime.combine(day, worktype.start_work_day.time())
	finish_work = start_work + work_duration

	return start_work <= now_datetime < finish_work


class _CalendarGridDay(MDLabel):
	''' Представление дня на сетке календаря '''

	def __init__(self, date: date, this_month: bool=True):
		self.date = date
		self.this_month = this_month
		self.is_select = False

		super().__init__()

	def select(self) -> None:
		''' Выделить '''
		self.is_select = True
		self.md_bg_color = (1, 0, 0, .2)

	def unselect(self) -> None:
		''' Снять выделение '''
		self.is_select = False
		self.md_bg_color = (0, 0, 0, 0)


class FDCalendar(MDBoxLayout):
	''' Поле отображения календаря с рабочими днями '''

	def __init__(self):
		self._calendar = Calendar()
		self._now_date = datetime.now().date()

		super().__init__()

		self._grid_elements: List[_CalendarGridDay] = []
		self._is_select_work_days = False
		self._work_days_params = {
			'work_day': None,
			'worktype': None,
			'vacation': None}
		self.update()

	@property
	def now_date(self) -> date:
		return self._now_date

	@now_date.setter
	def now_date(self, new_date: Union[date, datetime]) -> None:
		if not isinstance(new_date, (date, datetime)):
			raise ValueError('param \'new_date\' is not date type.')
		self._now_date = new_date

	def _fill_grid(self) -> None:
		''' Заполнить сетку календаря '''
		grid = self.ids.calendar_grid
		grid.clear_widgets()
		self._grid_elements.clear()

		for date in self._calendar.itermonthdates(self._now_date.year, self._now_date.month):
			this_month = date.month == self._now_date.month
			d = _CalendarGridDay(date=date, this_month=this_month)
			grid.add_widget(d)
			self._grid_elements.append(d)

		if self._is_select_work_days:
			self.select_work_days(**self._work_days_params)

	def _change_month_title(self) -> None:
		''' Изменить название месяца '''
		self.ids.month_title.text = MONTHS[self._now_date.month]

	def select_work_days(self, work_day: date, worktype: Worktype,
	                     vacation: Tuple[datetime.date]=None) -> None:
		''' Выделить рабочие дни '''
		if work_day is None or worktype is None:
			self.unselect_work_days()
			return

		self._is_select_work_days = True
		if vacation is None:
			s_vac = date(1, 1, 1)
			f_vac = date(1, 1, 1)
		else:
			s_vac, f_vac, *_ = vacation
		self._work_days_params = {
			'work_day': work_day,
			'worktype': worktype,
			'vacation': (s_vac, f_vac)}

		for calendar_day in self._grid_elements:
			is_work = is_work_day(calendar_day.date, work_day, worktype)
			if is_work and not(s_vac <= calendar_day.date <= f_vac):
				calendar_day.select()
			else:
				calendar_day.unselect()

	def unselect_work_days(self) -> None:
		''' Снять выделения рабочих дней '''
		self._is_select_work_days = False
		for calendar_day in self._grid_elements:
			calendar_day.unselect()

	def update(self) -> None:
		''' Обновить календарь '''
		self._fill_grid()
		self._change_month_title()

	def move_to_prev_month(self) -> None:
		''' Перевернуть календарь на месяц назад '''
		self._now_date = add_months(
			current_date=self._now_date,
			months_to_add=-1)
		self.update()

	def move_to_next_month(self) -> None:
		''' Перевернуть календарь на месяц вперед '''
		self._now_date = add_months(
			current_date=self._now_date,
			months_to_add=1)
		self.update()
