# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta


class Graph:
	def __init__(self, start_work_day: datetime, finish_work_day: datetime,\
		work_day_range: int, week_day_range: int):

		self._start_work_day = start_work_day
		self._finish_work_day = finish_work_day
		self._work_day_range = work_day_range
		self._week_day_range = week_day_range

		self.work_time = self._finish_work_day - self._start_work_day

	def calc_next_work_day(self) -> datetime:
		return self._start_work_day + timedelta(days=self._work_day_range) \
			 + timedelta(days=self._week_day_range)

	def __str__(self):
		return '{work_d}/{week_d} [{wt} hours]'.format(
			work_d=self._work_day_range,
			week_d=self._week_day_range,
			wt=self.work_time
		)


if __name__ == '__main__':
	now_date = datetime.now()

	x = datetime(year=now_date.year, month=now_date.month,
		day=25, hour=8)
	y = datetime(year=now_date.year, month=now_date.month,
		day=25, hour=17)

	grs = [Graph(x, y, 7-i, i) for i in range(1, 7)]
	grs.append(Graph(x, y, 1, 3))

	for gr in grs:
		print(gr, gr.calc_next_work_day())