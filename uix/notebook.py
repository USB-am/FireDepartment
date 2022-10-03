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


class FilterWorkingHuman():
	''' Фильтр работающих людей '''

	def __init__(self, humans: list):
		self.humans = humans

	def filter(self) -> list:
		output = []

		for human in self.humans:
			if human.worktype is None:
				continue

			print(human.title, human.work_day)
			if self._is_works(human):
				output.append(human)

		return output

	def _is_works(self, human: Human) -> bool:
		work_type = Worktype.query.get(human.worktype)
		work_day = human.work_day
		start_workday, finish_workday = self.__calc_work_day(work_type, work_day)

		is_work = start_workday <= datetime.now() < finish_workday

		return is_work

	def __calc_work_day(self, work_type: Worktype, work_day: datetime) -> tuple:
		def get_wk_bias(datetime_: datetime) -> int:
			''' Возвращает количество дней до текущей даты '''

			now_td = datetime.now().toordinal()
			acc_td = datetime_.toordinal()

			bias_value = (now_td - acc_td) - (now_td - acc_td) % 7

			return timedelta(days=bias_value)

		start_wd = work_type.start_work_day + get_wk_bias(work_day)
		start_a_work = start_wd + get_wk_bias(start_wd)
		finish_a_work = 1
		start_a_week = start_a_work + timedelta(days=work_type.work_day_range)

		print(start_a_work, start_a_week, end='\n'*2)

		return start_a_work, start_a_week


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
		today_workers = FilterWorkingHuman(self.element.humans)
		#sorted_humans = sorted(
		#	self.element.humans,
		#	key=self.__get_human_rank_priority,
		#	reverse=True)

		[scroll_layout.add_widget(HumansSelectedListElement(human)) \
			for human in today_workers.filter()]

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