from calendar import Calendar
from datetime import datetime, date

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from dateutil.relativedelta import relativedelta

from config import CALENDAR_FIELD


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


class _CalendarGridDay(MDLabel):
	''' Представление дня на сетке календаря '''

	def __init__(self, day: int, this_month: bool=True):
		self.day = day
		self.this_month = this_month

		super().__init__()

class FDCalendar(MDBoxLayout):
	''' Поле отображения календаря с рабочими днями '''

	def __init__(self):
		self._calendar = Calendar()
		self._now_date = datetime.now().date()

		super().__init__()

		self._fill_elements()

	@property
	def now_date(self) -> date:
		return self._now_date

	@now_date.setter
	def now_date(self, new_date: date) -> None:
		if not isinstance(new_date, date):
			raise ValueError('param \'new_date\' is not date type.')
		self._now_date = new_date

	def _fill_elements(self) -> None:
		''' Заполнить сетку календаря '''
		grid = self.ids.calendar_grid
		grid.clear_widgets()

		for date in self._calendar.itermonthdates(self._now_date.year, self._now_date.month):
			day = date.day
			this_month = date.month == self._now_date.month
			d = _CalendarGridDay(day=day, this_month=this_month)
			grid.add_widget(d)

	def _change_month_title(self) -> None:
		''' Изменить название месяца '''
		self.ids.month_title.text = MONTHS[self._now_date.month]

	def update(self) -> None:
		''' Обновить календарь '''
		self._fill_elements()
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
