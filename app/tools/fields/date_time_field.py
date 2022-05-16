# -*- coding: utf-8 -*-

import os
import datetime

from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDTimePicker, MDDatePicker

from config import PATTERNS_DIR, LOCALIZED


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
				range_: list) -> None:
		''' Update self._date and text to date_button '''

		self._date = date
		self.ids.date_button.text = date.strftime('%d.%m.%Y')

	def _update_time(self, instance: MDTimePicker, time: datetime.time) -> None:
		''' Update self._time and text to time_button '''

		self._time = time
		self.ids.time_button.text = time.strftime('%H:%M:%S')

	def clear(self) -> None:
		self._date = None
		self._time = None

	def get_value(self) -> datetime.datetime:
		''' Returns requested datetime '''

		try:
			return datetime.datetime(
				year=self._date.year,
				month=self._date.month,
				day=self._date.day,
				hour=self._time.hour,
				minute=self._time.minute)
		except AttributeError:
			pass