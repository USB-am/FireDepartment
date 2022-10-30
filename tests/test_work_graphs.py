# -*- coding: utf-8 -*-

from datetime import *
from dataclasses import dataclass
import unittest

from uix.notebook import *


work_graphs = {
	'1/3': Worktype(
		title='1/3',
		start_work_day=datetime(2022, 10, 3, 9),
		finish_work_day=datetime(2022, 10, 4, 9),
		work_day_range=1,
		week_day_range=3
	),
	'5/2': Worktype(
		title='5/2',
		start_work_day=datetime(2022, 10, 3, 8),
		finish_work_day=datetime(2022, 10, 3, 17),
		work_day_range=5,
		week_day_range=2
	),
	'All': Worktype(
		title='All',
		start_work_day=datetime(2022, 10, 3, 0),
		finish_work_day=datetime(2022, 10, 4, 0),
		work_day_range=7,
		week_day_range=0
	)
}
humans = [
	Human(
		title='Human #1',
		work_day=date(2022, 11, 10),
		work_type=work_graphs['1/3']
	),
	Human(
		title='Human #2',
		work_day=date(2022, 11, 14),
		work_type=work_graphs['5/2']
	),
	Human(
		title='Human #3',
		work_day=date(2022, 11, 14),
		work_type=work_graphs['All']
	)
]


class TestFilter(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.human1 = humans[0]
		self.human2 = humans[1]
		self.human3 = humans[2]
		self.filter = Filter(humans)

	def test_get_default_wk_h1(self):
		h_wk = self.filter._get_default_wk(self.human1)
		h_wk_test = (h_wk.start_day, h_wk.finish_day)
		h_val = (date(2022, 11, 10), date(2022, 11, 13))
		self.assertEqual(h_wk_test, h_val)

	def test_get_default_wk_h2(self):
		h_wk = self.filter._get_default_wk(self.human2)
		h_wk_test = (h_wk.start_day, h_wk.finish_day)
		h_val = (date(2022, 11, 14), date(2022, 11, 20))
		self.assertEqual(h_wk_test, h_val)

	def test_get_default_wk_h3(self):
		h_wk = self.filter._get_default_wk(self.human3)
		h_wk_test = (h_wk.start_day, h_wk.finish_day)
		h_val = (date(2022, 11, 14), date(2022, 11, 20))
		self.assertEqual(h_wk_test, h_val)


	def test_get_bias_wk_h1(self):
		h_wk = self.filter._get_default_wk(self.human1)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 11, 25))
		w_wk_test = (working_wk.start_day, working_wk.finish_day)
		h_val = (date(2022, 11, 22), date(2022, 11, 25))

		self.assertEqual(w_wk_test, h_val)

	def test_get_bias_wk_h2(self):
		h_wk = self.filter._get_default_wk(self.human2)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 11, 26))
		w_wk_test = (working_wk.start_day, working_wk.finish_day)
		h_val = (date(2022, 11, 21), date(2022, 11, 27))

		self.assertEqual(w_wk_test, h_val)

	def test_get_bias_wk_h3(self):
		h_wk = self.filter._get_default_wk(self.human3)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 10, 26))
		w_wk_test = (working_wk.start_day, working_wk.finish_day)
		h_val = (date(2022, 10, 24), date(2022, 10, 30))

		self.assertEqual(w_wk_test, h_val)


	def test_get_working_days_h1(self):
		h_wk = self.filter._get_default_wk(self.human1)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 11, 25))
		working_days = self.filter._get_working_days(working_wk, self.human1.work_type)
		h_val = [WorkingDay(datetime(2022, 11, 22, 9), datetime(2022, 11, 23, 9)),]

		self.assertEqual(working_days, h_val)

	def test_get_working_days_h2(self):
		h_wk = self.filter._get_default_wk(self.human2)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 11, 25))
		working_days = self.filter._get_working_days(working_wk, self.human2.work_type)
		h_val = [WorkingDay(datetime(2022, 11, 21+i, 8), datetime(2022, 11, 21+i, 17)) for i in range(5)]

		self.assertEqual(working_days, h_val)

	def test_get_working_days_h3(self):
		h_wk = self.filter._get_default_wk(self.human3)
		working_wk = self.filter._get_bias_wk(h_wk, date(2022, 11, 25))
		working_days = self.filter._get_working_days(working_wk, self.human3.work_type)
		h_val = [WorkingDay(datetime(2022, 11, 21+i, 0), datetime(2022, 11, 22+i, 0)) for i in range(7)]

		self.assertEqual(working_days, h_val)


if __name__ == '__main__':
	unittest.main()