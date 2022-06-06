# -*- coding: utf-8 -*-

import os
import datetime

from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDTimePicker, MDDatePicker

from config import PATTERNS_DIR, LOCALIZED
from app.exceptions.check_exceptions import check_none_value


path_to_kv_file = os.path.join(PATTERNS_DIR, 'fields', 'date_time_field.kv')
Builder.load_file(path_to_kv_file)


class DateTimeField(MDBoxLayout):
	''' Asks the user for a date and time. '''

	icons = {
		'start_work_day': 'briefcase-clock',
		'finish_work_day': 'bus-clock',
	}

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(self.title)
		self.icon = self.icons.get(self.title, 'briefcase-clock')

		super().__init__()

		self._date = None
		self._time = None

		# Create pickers
		self._date_dialog = MDDatePicker()
		self._time_dialog = MDTimePicker()

		# Bind save methods
		self._date_dialog.bind(on_save=self._update_date)
		self._time_dialog.bind(on_save=self._update_time)

		# Bind buttons to open pickers
		self.ids.date_button.bind(on_press=self._open_date_dialog)
		self.ids.time_button.bind(on_press=self._open_time_dialog)

	def _open_date_dialog(self, instance: MDRaisedButton) -> None:
		''' Open MDDatePicker dialog '''

		self._date_dialog.open()

	def _open_time_dialog(self, instance: MDRaisedButton) -> None:
		''' Open MDTimePicker dialog '''

		self._time_dialog.open()

	def _update_date(self, instance: MDDatePicker, date: datetime.date,\
				range_: list=[]) -> None:
		''' Update self._date and text to date_button '''

		self._date = date
		self.update_value_text()

	def _update_time(self, instance: MDTimePicker, time: datetime.time) -> None:
		''' Update self._time and text to time_button '''

		self._time = time
		self.update_value_text()

	def update_value_text(self) -> None:
		self.ids.fill_data.text = self.__get_markup_str()

	def __get_markup_str(self) -> str:
		def check_none(value: datetime.datetime, type_: str, ftime: str) -> str:
			if value is None:
				return 'dd.mm.yyyy' if type_ == 'date' else 'HH:MM:SS'
			else:
				return '[b]{}[/b]'.format(value.strftime(ftime))

		return '\n'.join((
			check_none(self._date, 'date', '%d.%m.%Y'),
			check_none(self._time, 'time', '%H:%M:%S')
		))

	def clear(self) -> None:
		self._date = None
		self._time = None

		self.update_value_text()

	def get_value(self) -> datetime.datetime:
		''' Returns requested datetime '''

		try:
			return datetime.datetime(
				year=self._date.year,
				month=self._date.month,
				day=self._date.day,
				hour=self._time.hour,
				minute=self._time.minute)
		except AttributeError as e:
			print(f'[{e.__class__.__name__}] {e}')

	@check_none_value
	def set_value(self, date: datetime.datetime) -> None:
		''' Set value and update button states '''

		self._update_date(None, date.date())
		self._update_time(None, date.time())