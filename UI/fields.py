# -*- coding: utf-8 -*-

from os.path import join as os_join
from calendar import Calendar
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label

from config import PATTERNS_DIR


path_to_kv_file = os_join(PATTERNS_DIR, 'fields.kv')
Builder.load_file(path_to_kv_file)


class StringField(BoxLayout):
	def __init__(self, title: str):
		self.title = title

		super().__init__()

	def set_value(self, value: str) -> None:
		self.ids.text_input.text = value

	def get_value(self) -> str:
		return self.ids.text_input.text


class PhoneField(BoxLayout):
	def __init__(self, title: str):
		self.title = title

		super().__init__()

	def set_value(self, value: str) -> None:
		if value is None:
			value = ''

		self.ids.text_input.text = value

	def get_value(self) -> str:
		return self.ids.text_input.text


class CalendarDate(ToggleButton):
	def __init__(self, date: datetime.date):
		self.date = date

		super().__init__(
			text=self.__get_text(),
			size_hint=(None, None),
			size=(30, 30),
			font_size=14,
			group='calendar',
			markup=True
		)


	def __get_text(self) -> str:
		if self.date.month != datetime.now().month:
			return f'[color=202325]{self.date.day}[/color]'

		return str(self.date.day)


class CalendarField(BoxLayout):
	CALENDAR = Calendar()
	NOW_DATE = datetime.now()

	def __init__(self, title: str):
		self.title = title

		super().__init__()

		self.fill_calendar_table()

	def fill_calendar_table(self) -> None:
		month_days = list(self.CALENDAR.itermonthdates(
			self.NOW_DATE.year, self.NOW_DATE.month
		))
		container = self.ids.calendar_table

		for week_day in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']:
			container.add_widget(Label(
				size_hint=(None, None),
				size=(30, 30),
				text=week_day
			))

		for day in month_days:
			container.add_widget(CalendarDate(day))

	def set_value(self, value) -> None:
		print(value, type(value))


class RadioItem(BoxLayout):
	STATES = {
		'down': False,
		'normal': True
	}

	def __init__(self, title: str):
		self.title = title

		super().__init__()

	def change_state(self) -> None:
		if self.STATES[self.ids.check_box.state]:
			self.ids.check_box.state = 'down'
		else:
			self.ids.check_box.state = 'normal'

	def get_value(self) -> bool:
		return self.ids.check_box.state == 'down'


class RadioField(BoxLayout):
	POINTS = {
		0: '5/2',
		1: '1/3',
		2: 'Всегда'
	}

	def __init__(self, title):
		self.title = title

		super().__init__()

		self.fill_radiobuttons()

	def fill_radiobuttons(self):
		for point in range(3):
			field = RadioItem(self.POINTS[point])
			self.add_widget(field)

	def set_value(self, value: int) -> None:
		if value is not None:
			childrens = self.children[::-1][1:]
			childrens[value].change_state()

	def get_value(self) -> int:
		childrens = self.children[::-1][1:]

		for num, children in enumerate(childrens):
			if children.get_value():
				return num


class ForeignKeyField(BoxLayout):
	def __init__(self, title):
		self.title = title
		super().__init__()

	def set_value(self, value):
		pass