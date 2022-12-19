import os
from datetime import *
from dataclasses import dataclass

from kivy.lang import Builder
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

from data_base import Emergency, Human, Rank, Worktype, Calls
from uix import FDScrollFrame
from uix.dialog import FDDialog, HumanDialogContent
from uix.fields import TripleCheckbox, DescriptionField
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

		return self._is_date_in_working_wk(dt, working_days)

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

	def _get_working_days(self, wk: Week, work_type: Worktype) -> list:	# list[WorkingDay]
		work_days = range(work_type.work_day_range)
		output = []

		for num, day in zip(work_days, wk):
			swd = work_type.start_work_day.time()
			start = datetime(day.year, day.month, day.day, swd.hour, swd.minute)
			finish = start + (work_type.finish_work_day - work_type.start_work_day)
			working_day = WorkingDay(start, finish)
			output.append(working_day)

		return output

	def _is_date_in_working_wk(self, dt: datetime, week: list) -> bool:
		for working_day in week:
			if working_day.start <= dt < working_day.finish:
				return True

		return False


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

	def update(self) -> None:
		pass


class EmergencyDecriptionField(MDTextField):
	''' Многострочное поле для описания вызова '''

	def __init__(self, title: str):
		self.title = title
		self.display_text = LOCALIZED.translate(title)

		super().__init__(
			size_hint=(1, 1),
			hint_text=self.display_text,
			multiline=True,
			mode='rectangle'
		)


class DropupLayout(MDBoxLayout):
	''' Выдвигающийся снизу список '''

	def __init__(self, title: str, content: MDBoxLayout):
		self.title = title
		self.display_text = LOCALIZED.translate(title)
		self.content = content

		super().__init__()
		self.add_widget(self.content)

		self.state = False

		self.ids.button.bind(on_release=lambda e: self._open_layout())

	def _open_layout(self) -> None:
		button = self.ids.button

		if self.state:
			self.state = False
			button.icon = 'chevron-up'
			self.height = 50
		else:
			self.state = True
			button.icon = 'chevron-down'
			self.height = 400


class FDEmergencyTab(MDBoxLayout, MDTabsBase):
	''' Вкладка с информацией о вызовах '''

	def __init__(self, call: Calls):
		self.call = call
		self.element = Emergency.query.get(call.emergency)
		self.title = self.element.title
		self.workers_filter = Filter(self.element.humans)

		super().__init__(orientation='vertical')

		self.setup()

	def setup(self) -> None:
		# scroll_layout = self.ids.scroll_layout

		# now_date = datetime.now()
		# today_workers = self.workers_filter.get_working(now_date)
		# [scroll_layout.add_widget(HumansSelectedListElement(human)) \
		# 	for human in today_workers]

		# Description layout
		self.add_widget(EmergencyDecriptionField(
			title=LOCALIZED.translate('Description field')
		))

		# Dropup layout
		self.add_widget(DropupLayout(
			title=LOCALIZED.translate('Participants'),
			content=MDBoxLayout()
		))

	def open_dropup_layout(self) -> None:
		self.ids.open_button.icon = 'chevron-down'
		layout = self.ids.dropup_layout
		layout.height = 400

	def update(self) -> None:
		now_date = datetime.now()

		for child in self.ids.scroll_layout.children[:-1]:
			if not self.workers_filter.is_working(now_date, child.human):
				self.ids.scroll_layout.remove_widget(child)


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