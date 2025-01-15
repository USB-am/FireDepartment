import unittest
from datetime import datetime, date

from kivymd.uix.boxlayout import MDBoxLayout

from tests import AppTest
from data_base import Worktype
from ui.field import calendar as Calendar
from ui.field.date import FDDate
from ui.field.select import FDSelect


class TestFDCalendar(unittest.TestCase):
	''' Тесты FDCalendar '''

	@classmethod
	def setUpClass(cls):
		cls.NOW_DATE = datetime(2024, 12, 10)
		cls.app = AppTest()

		cls.calendar = Calendar.FDCalendar()
		cls.calendar._now_date = cls.NOW_DATE

		cls.app.screen.add_widget(cls.calendar)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.calendar)

	def setUp(self):
		self.calendar._now_date = self.NOW_DATE

	def test_next_month(self):
		now_month = self.calendar.now_date.month
		self.calendar.move_to_next_month()
		next_month = self.calendar.now_date.month

		self.assertEqual((now_month + 1) % 12, next_month)

	def test_prev_month(self):
		now_month = self.calendar.now_date.month
		self.calendar.move_to_prev_month()
		prev_month = self.calendar.now_date.month
		current_month = now_month - 1 if now_month - 1 > 0 else 12

		self.assertEqual(current_month, prev_month)

	def test_add_month(self):
		func_result = Calendar.add_months(self.NOW_DATE.date(), 1)
		expected = date(
			year=self.NOW_DATE.year if self.NOW_DATE.month + 1 <= 12 else self.NOW_DATE.year + 1,
			month=(self.NOW_DATE.month + 1) % 12,
			day=self.NOW_DATE.day)
		self.assertEqual(func_result, expected)

	def test_is_work_day(self):
		start_date = datetime(year=2024, month=12, day=1, hour=9)
		finish_date = datetime(year=2024, month=12, day=2, hour=9)
		wt = Worktype(
			title='1/1',
			start_work_day=start_date,
			finish_work_day=finish_date,
			work_day_range=1,
			week_day_range=1
		)

		for day in range(1, 10):
			test_date = date(year=2024, month=12, day=day)
			result = Calendar.is_work_day(test_date, start_date.date(), wt)
			self.assertEqual(result, bool(day%2))


if __name__ == '__main__':
	unittest.main()
