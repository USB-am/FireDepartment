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
	humans: list

	def get_on_date(self, datetime_: datetime) -> list:
		output = [human for human in self.humans if self._is_works(datetime_, human)]

		return output

	def _is_works(self, date_: datetime, human: Human) -> bool:
		return int(human.title[-1]) % 2


def main():
	humans = list(init_humans())
	filter_ = Filter(humans)
	today_workers = filter_.get_on_date(datetime.now())
	[print(worker) for worker in today_workers]


if __name__ == '__main__':
	main()