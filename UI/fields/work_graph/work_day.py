# -*- coding: utf-8 -*-

import os
from datetime import date, datetime

from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker

from settings import settings as Settings
from settings import LANG


path_to_kv_file = os.path.join(
	Settings.PATTERNS_DIR, 'fields', 'work_day.kv')
Builder.load_file(path_to_kv_file)


class SelectDate(MDDatePicker):
	def __init__(self, callback):
		self.callback_ = callback

		super().__init__()

	def on_save(self, date: date, date_range: list) -> None:
		self.callback_(date)
		super().on_save()


class WorkDayField(MDBoxLayout):
	def __init__(self, title: str):
		self.column_name = title
		self.title = title.title()
		self.info_text = LANG.get(self.title, '')

		self.now_date = datetime.now().date()

		super().__init__()

		self.ids.open_calendar_button.bind(on_press=self.open_calendar)

	def open_calendar(self, instance) -> None:
		date_dialog = SelectDate(self.update_now_date)
		date_dialog.open()

	def update_now_date(self, date: date) -> None:
		self.now_date = date

		self.update_label_date()

	def update_label_date(self) -> None:
		self.ids.show_date.text = self.now_date.strftime('%d.%m.%Y')

	def get_value(self) -> date:
		return self.now_date