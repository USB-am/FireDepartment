import os
from datetime import *
from dataclasses import dataclass

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


class Week(list):
	def __init__(self, start_day: date, finish_day: date):
		super().__init__()

		self.start_day = start_day
		self.finish_day = finish_day
		self.setup()

	def setup(self):
		days_count = (self.finish_day - self.start_day).days + 1

		for i in range(days_count):
			self.append(self.start_day + timedelta(days=i))

	def __str__(self):
		return f'{self.start_day} -> {self.finish_day}'


@dataclass
class WorkingDay():
	start: datetime
	finish: datetime


class Filter():
	def __init__(self, humans: list):
		self.humans = humans

	def get_working(self, dt: datetime) -> list:
		return [human for human in self.humans if self.is_working(dt, human)]

	def is_working(self, dt: datetime, human: Human) -> bool:
		human_wk_default = self._get_default_wk(human)
		working_wk = self._get_bias_wk(human_wk_default, dt.date())
		working_days = self._get_working_days(working_wk, Worktype.query.get(human.worktype))

		return working_days

	def _get_default_wk(self, human: Human) -> Week:
		''' Возвращает неделю, начинающуюся с human.work_day '''
		wt: Worktype = Worktype.query.get(human.worktype)
		wd: date = human.work_day
		wk_length = wt.work_day_range + wt.week_day_range

		return Week(wd, wd + timedelta(days=wk_length - 1))

	def _get_bias_wk(self, wk: Week, dt: date) -> Week:
		''' Смещает неделю (wk) так, чтобы она включала в себя дату dt '''
		wk_length = len(wk)
		bias = (dt.toordinal() - wk.start_day.toordinal()) // wk_length

		swk = wk.start_day + timedelta(days=bias*wk_length)
		fwk = swk + timedelta(days=wk_length-1)

		return Week(swk, fwk)

	def _get_working_days(self, wk: Week, work_type: Worktype) -> list:
		work_days = range(work_type.work_day_range)
		output = []

		for num, day in zip(work_days, wk):
			swd = work_type.start_work_day.time()
			start = datetime(day.year, day.month, day.day, swd.hour, swd.minute)
			finish = start + (work_type.finish_work_day - work_type.start_work_day)
			working_day = WorkingDay(start, finish)
			output.append(working_day)

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


class FDEmptyTab(MDFloatLayout, MDTabsBase):
	''' Пуская вкладка '''

	def __init__(self, title_: str):
		self.title = 'Empty'
		self.display_text = '[b]{empty}[/b]\n[i]{comment}[/i]'.format(
			empty=LOCALIZED.translate('Empty'),
			comment=LOCALIZED.translate(title_))

		super().__init__()


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

		today_workers = workers_filter.get_working(datetime.now())
		[scroll_layout.add_widget(HumansSelectedListElement(human)) \
			for human in today_workers]


class FDNoteBook(MDTabs):
	''' Виджет с вкладками '''

	def __init__(self, empty_tab_text: str='', **options):
		super().__init__(**options)

		self.empty_tab_text = empty_tab_text

		self._current_tab = None
		self.bind(on_tab_switch=lambda tabs, tab, tab_label, tab_text:
		          self.update_current_tab(tab))

		self.add_widget(FDEmptyTab(self.empty_tab_text))
		self.switch_to_last_tab()

	def add_tab(self, tab: MDTabsBase) -> None:
		self.add_widget(tab)

		empty_tabs = self.get_empty_tabs()
		if empty_tabs:
			[self.remove_widget(tab) for tab in empty_tabs]

	def close_tab(self, tab: MDTabsBase) -> None:
		if len(self.get_tab_list()) > 1:
			self.remove_widget(tab)

		else:
			self.add_widget(FDEmptyTab(self.empty_tab_text))
			self.switch_to_last_tab()
			# self.remove_widget(tab)

	def switch_to_last_tab(self) -> None:
		last_tab = self.get_tab_list()[-1]
		self.switch_tab(last_tab)
		self.current_tab = last_tab

	def get_empty_tabs(self) -> list:
		tabs = self.get_tab_list()
		empties = [tab for tab in tabs if isinstance(tab.tab, FDEmptyTab)]

		return empties

	def update_current_tab(self, tab: MDTabsBase) -> None:
		self.current_tab = tab

	@property
	def current_tab(self) -> MDTabsBase:
		return self._current_tab

	@current_tab.setter
	def current_tab(self, tab: MDTabsBase) -> None:
		self._current_tab = tab