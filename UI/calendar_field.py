# -*- coding: utf-8 -*-

import os
import calendar
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

import config as Config


Builder.load_file(os.path.join(Config.PATTERNS_DIR, 'calendar.kv'))

year = datetime.now().year
month = datetime.now().month
_CALENDAR = calendar.Calendar()


class CalendarDayButton(ToggleButton):
	backgrounds = {
		True: (1, 0, 0, 1),
		False: (1, 1, 1, 1)
	}

	def __init__(self, date: datetime.date, active: bool=False):
		self.date = date
		self.show_text = self.__get_show_text()
		self.background_color = self.backgrounds[active]

		super().__init__(markup=True, group='days')

	def __get_show_text(self) -> str:
		if self.date.month != month:
			result = f'[color=bfbfbf]{self.date.day}[/color]'
		else:
			result = f'{self.date.day}'

		return result


class Calendar(BoxLayout):
	def __init__(self):
		super().__init__()

		self.fill_calendar_table()

	def fill_calendar_table(self) -> None:
		container = self.ids.calendar_table

		now_month_calendar = [day for day in _CALENDAR.itermonthdates(year, month)]
		for day in now_month_calendar:
			container.add_widget(CalendarDayButton(day))