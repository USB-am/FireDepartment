from calendar import Calendar

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from config import CALENDAR_FIELD


Builder.load_file(CALENDAR_FIELD)


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

		super().__init__()

		for i in range(31):
			day = _CalendarGridDay(day=i+1, this_month=bool((i+1)%4))
			self.ids.calendar_grid.add_widget(day)
