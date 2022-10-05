import os
from datetime import datetime, timedelta

from kivy.lang import Builder
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

from data_base import Emergency, Human, Rank, Worktype
from uix import FDScrollFrame
from uix.dialog import FDDialog, HumanDialogContent
from uix.fields import TripleCheckbox
from config import UIX_KV_DIR, LOCALIZED


path_to_kv_file = os.path.join(UIX_KV_DIR, 'notebook.kv')
Builder.load_file(path_to_kv_file)


class Filter():
	''' Фильтр работников '''
	def __init__(self, humans: list):
		self.humans = humans

	def get_on_date(self, datetime_: datetime) -> list:
		output = [human for human in self.humans if self._is_works(datetime_, human)]

		return output

	def _is_works(self, datetime_: datetime, human: Human) -> bool:
		work_day = human.work_day

		if human.worktype is None:
			return False

		wt = Worktype.query.get(human.worktype)

		week_bias = self.__calc_week_bias(wt, work_day)
		today_week = self.__get_today_week(datetime_, week_bias)
		work_days = self.__get_work_days(wt, today_week)
		# print(work_days, datetime_, sep='->')
		output = work_days[0] <= datetime_ < work_days[-1]

		# return datetime_ in work_days
		return output

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


class HumansSelectedListElement(MDBoxLayout):
	''' Элемент списка с людьми, которым надо позвонить '''

	def __init__(self, human: Human):
		self.human = human

		super().__init__()

		self.setup()

	def setup(self) -> None:
		# Init dialog
		dialog_button = MDRaisedButton(text=LOCALIZED.translate('Ok'))
		self.dialog = FDDialog(
			title=self.human.title,
			content=HumanDialogContent(self.human),
			buttons=[dialog_button,])

		dialog_button.bind(on_release=lambda e: self.dialog.dismiss())
		self.ids.expansion_panel.bind(on_release=lambda e: self.dialog.open())

		# Init TripleCheckbox
		self.triple_checkbox = TripleCheckbox(
			state_normal='phone-settings-outline',
			state_ok='phone-in-talk',
			state_cancel='phone-cancel')
		self.ids.checkbox_container.add_widget(self.triple_checkbox)
		self.triple_checkbox.bind(on_release=lambda e: self.update_color())

	@property
	def phone_1(self) -> str:
		phone = self.human.phone_1
		return '-' if phone is None else phone

	@property
	def phone_2(self) -> str:
		phone = self.human.phone_2
		return '-' if phone is None else phone

	def update_color(self) -> None:
		now_state = self.triple_checkbox.increment

		if now_state == 0:
			self.md_bg_color = (0, 1, 0, .3)
		elif now_state == 1:
			self.md_bg_color = (1, 0, 0, .3)
		else:
			self.md_bg_color = (1, 1, 1, 0)


class FDEmergencyTab(MDFloatLayout, MDTabsBase):
	''' Вкладка с информацией о вызовах '''

	def __init__(self, element: Emergency):
		self.element = element
		self.title = element.title

		super().__init__()

		self.setup()

	def setup(self) -> None:
		scroll_layout = self.ids.scroll_layout
		workers_filter = Filter(self.element.humans)

		today_workers = workers_filter.get_on_date(datetime.now())
		[scroll_layout.add_widget(HumansSelectedListElement(human)) \
			for human in today_workers]

	def get_today_workers(self) -> list:
		output = []
		humans = Human.query.all()

		for human in humans:
			worktype_id = human.worktype

			if worktype_id is None:
				continue

			wt = Worktype.query.get(worktype_id)
			start_work_day = wt.start_work_day
			finish_work_day = wt.finish_work_day

			if start_work_day <= datetime.now() < finish_work_day:
				print(human.title)
			yield human

	def __get_human_rank_priority(self, human: Human) -> int:
		rank = Rank.query.get(human.rank)

		if rank is None:
			return 0
		return rank.priority


class FDNoteBook(MDTabs):
	''' Виджет с вкладками '''