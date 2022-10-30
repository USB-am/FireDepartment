# -*- coding: utf-8 -*-

from datetime import *
from dataclasses import dataclass
import unittest


@dataclass
class Worktype():
	title: str
	start_work_day: datetime
	finish_work_day: datetime
	work_day_range: int
	week_day_range: int

	def __str__(self):
		return self.title


@dataclass
class Human():
	title: str
	work_day: date
	work_type: Worktype

	def __str__(self):
		return self.title


class Filter():
	def __init__(self, humans: list):
		self.humans = humans

	def get_working(self, dt: datetime) -> list:
		return [human for human in self.humans if self.is_working(dt, human)]

	def is_working(self, dt: datetime, human: Human) -> bool:
		wk = self._get_wk(human)
		working_wk = self._get_working_wk(wk, dt.date())
		working_days = self._get_working_days(working_wk, human.work_type)

		wd_length = (working_days[1] - working_days[0]).days
		for i in range(wd_length + 1):
			day = working_days[0] + timedelta(days=i)
			swt, fwt = self._get_working_time(day, human.work_type)

			if swt <= dt < fwt:
				return True

		return False

	def _get_wk(self, human: Human) -> tuple:
		''' Возвращает все дни в соответствии с work_type '''
		wt: Worktype = human.work_type
		bias = sum((wt.work_day_range, wt.week_day_range))
		start_wk = human.work_day
		finish_wk = human.work_day + timedelta(days=bias-1)

		return (start_wk, finish_wk)

	def _get_working_wk(self, wk: tuple, day: date) -> tuple:
		swk, fwk = wk
		wk_length = (fwk - swk).days

		bias = abs(day.toordinal() - swk.toordinal()) // wk_length

		first_work_day = swk + timedelta(days=wk_length * bias + 1)	# ?
		last_work_day = first_work_day + timedelta(days=wk_length)

		return (first_work_day, last_work_day)

	def _get_working_days(self, wk: tuple, work_type: Worktype) -> tuple:
		''' Возвращает только рабочие дни недели '''
		swk, _ = wk
		length = work_type.work_day_range - 1

		output = (swk, swk + timedelta(days=length))

		return output

	def _get_working_time(self, dt: date, work_type: Worktype) -> tuple:
		''' Возвращает рабочее время на день dt '''
		swd: datetime = work_type.start_work_day
		fwd: datetime = work_type.finish_work_day

		wd_length = fwd - swd
		dt_start = datetime(dt.year, dt.month, dt.day, swd.hour, swd.minute)
		dt_finish = dt_start + wd_length

		return (dt_start, dt_finish)


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
		work_day_range=1,
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

	def test_get_wk_human_1(self):
		h_wk = self.filter._get_wk(self.human1)
		h_val = (date(2022, 11, 10), date(2022, 11, 13))
		self.assertEqual(h_wk, h_val)

	def test_wk_bias_human_1(self):
		wk = self.filter._get_wk(self.human1)
		h_val = (date(2022, 11, 14), date(2022, 11, 17))
		working_wk = self.filter._get_working_wk(wk, date(2022, 11, 15))

		self.assertEqual(working_wk, h_val)

	def test_get_working_days_human1(self):
		wk = self.filter._get_wk(self.human1)
		h_val = (date(2022, 11, 10), date(2022, 11, 10))
		working_wk = self.filter._get_working_wk(wk, self.human1.work_day)
		working_days = self.filter._get_working_days(working_wk, self.human1.work_type)

		self.assertEqual(working_days, h_val)

	def test_get_working_time_human1(self):
		h_val = (datetime(2022, 11, 14, 9), datetime(2022, 11, 15, 9))
		working_time = self.filter._get_working_time(date(2022, 11, 14), self.human1.work_type)

		self.assertEqual(working_time, h_val)

	def test_is_working_human1(self):
		is_working = self.filter.is_working(datetime(2022, 11, 14, 10), self.human1)

		self.assertEqual(is_working, False)


if __name__ == '__main__':
	unittest.main()