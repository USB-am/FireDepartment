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
		# cls.NOW_DATE = datetime.now().date()
		cls.NOW_DATE = datetime(2024, 12, 10)
		cls.app = AppTest()
		cls.date_field = FDDate(
			icon='account',
			title='Test FDDate',
			btn_text='test btn')
		cls.date_field.set_value(cls.NOW_DATE)
		cls.worktype_field = FDSelect(
			title='Test FDSelect',
			dialog_content=MDBoxLayout(),
			model=Worktype,
			group='test_worktype_group')
		cls.worktype_field.set_value(Worktype.query.first())
		cls.calendar = Calendar.FDCalendar(
			from_date_field=cls.date_field,
			worktype_field=cls.worktype_field)

		cls.app.screen.add_widget(cls.calendar)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.calendar)

	def setUp(self):
		self.calendar.update(self.NOW_DATE)

	def test_next_month(self):
		now_month = self.calendar.now_date.month
		self.calendar.next_month()
		next_month = self.calendar.now_date.month

		self.assertEqual((now_month + 1) % 12, next_month)

	def test_prev_month(self):
		now_month = self.calendar.now_date.month
		self.calendar.prev_month()
		prev_month = self.calendar.now_date.month
		current_month = now_month - 1 if now_month - 1 > 0 else 12

		self.assertEqual(current_month, prev_month)

	def test_add_month(self):
		func_result = Calendar.add_months(self.NOW_DATE, 1)
		expected = date(
			year=self.NOW_DATE.year if self.NOW_DATE.month + 1 <= 12 else self.NOW_DATE.year + 1,
			month=(self.NOW_DATE.month + 1) % 12,
			day=self.NOW_DATE.day)
		self.assertEqual(func_result, expected)


if __name__ == '__main__':
	unittest.main()
