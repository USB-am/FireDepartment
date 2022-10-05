from datetime import datetime, timedelta, date
from dataclasses import dataclass


@dataclass
class Worktype():
	title: str
	start_work_day: datetime
	finish_work_day: datetime
	work_day_range: int
	week_day_range: int

	def __str__(self):
		return self.title


class Human:
	def __init__(self, title: str, worktype: Worktype, work_day: date):
		self.title = title
		self.worktype = worktype
		self.work_day = work_day

	def __str__(self):
		return f'{self.title} - {self.worktype.title}'


def init_humans() -> list:
	wt_5_2 = Worktype(
		title='5/2',
		start_work_day=datetime(2022, 9, 26, 8),
		finish_work_day=datetime(2022, 9, 26, 6),
		work_day_range=5,
		week_day_range=2)
	wt_1_3 = Worktype(
		title='1/3',
		start_work_day=datetime(2022, 9, 26, 9),
		finish_work_day=datetime(2022, 9, 27, 9),
		work_day_range=1,
		week_day_range=3)

	for i in range(10):
		wt = wt_5_2 if i%2 else wt_1_3

		human = Human(
			title=f'Human #{i+1}',
			worktype=wt,
			work_day=date(2022, 9, i+1))

		yield human


@dataclass
class Filter():
	''' Фильтр работников '''
	humans: list

	'''
	TODO:
		+ 1. Сделать смещение графика работы относительно рабочего дня работника;
		2. Найти диапазон недели, в которую будет входить необходимая дата;
		3. Из диапазона недели определить, является ли день рабочим;
		4. Из дня (п.3) сделать выборку по времени работы
	'''

	def get_on_date(self, datetime_: datetime) -> list:
		output = [human for human in self.humans if self._is_works(datetime_, human)]

		return output

	def _is_works(self, datetime_: datetime, human: Human) -> bool:
		work_day = human.work_day
		wt = human.worktype	# Worktype.query.get(human.worktype)

		week_bias = self.__calc_week_bias(wt, work_day)
		today_week = self.__get_today_week(datetime_, week_bias)
		work_days = self.__get_work_days(wt, today_week)

		return datetime_.date() in work_days

	def __calc_week_bias(self, work_type: Worktype, work_day: datetime) -> tuple:
		swd = work_day
		work_week_length = work_type.work_day_range + work_type.week_day_range
		fwd = swd + timedelta(days=work_week_length)

		return (swd, fwd)

	def __get_today_week(self, day: datetime, bias_week: tuple) -> tuple:
		swd, fwd = bias_week

		swd_count = swd.toordinal()
		fwd_count = fwd.toordinal()
		day_count = day.toordinal()
		week_length = fwd_count - swd_count

		bias = (day_count - swd_count) // week_length

		out_swd = swd + timedelta(days=bias * week_length)
		out_fwd = out_swd + timedelta(days=week_length)

		return (out_swd, out_fwd)

	def __get_work_days(self, work_type: Worktype, work_week: tuple) -> tuple:
		swd, fwd = work_week
		wd_count = work_type.work_day_range

		output = tuple([swd + timedelta(days=day_count) \
			for day_count in range(wd_count)])

		return output


def main():
	humans = list(init_humans())
	filter_ = Filter(humans)
	today_workers = filter_.get_on_date(datetime.now())
	[print(worker) for worker in today_workers]


if __name__ == '__main__':
	main()