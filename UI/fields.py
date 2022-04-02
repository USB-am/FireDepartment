# -*- coding: utf-8 -*-

from os.path import join as os_join
from calendar import Calendar
from datetime import datetime
from typing import Union

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from sqlalchemy.orm.collections import InstrumentedList

import config as Config
import db_models


path_to_kv_file = os_join(Config.PATTERNS_DIR, 'fields.kv')
Builder.load_file(path_to_kv_file)


class StringField(BoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.view_text = Config.LANG.get(self.title.title(), '[Неизвестно]')

		super().__init__()

	def set_value(self, db_row, key: str) -> None:
		value = getattr(db_row, key)

		if value is None:
			value = ''

		self.ids.text_input.text = value

	def get_value(self) -> Union[str, None]:
		result = self.ids.text_input.text

		if result:
			return result


class TextField(BoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.view_text = Config.LANG.get(self.title.title(), '[Неизвестно]')

		super().__init__()

	def set_value(self, db_row, key: str) -> None:
		value = getattr(db_row, key)

		if value is None:
			value = ''

		self.ids.text_input.text = value

	def get_value(self) -> str:
		return self.ids.text_input.text


class PhoneField(BoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.view_text = Config.LANG.get(self.title.title(), '[Неизвестно]')

		super().__init__()

	def set_value(self, db_row, key: str) -> None:
		value = getattr(db_row, key)

		if value is None:
			value = ''

		self.ids.text_input.text = value

	def get_value(self) -> str:
		result = self.ids.text_input.text

		if result:
			return result


class CalendarDate(ToggleButton):
	def __init__(self, date: datetime.date):
		self.date = date

		super().__init__(
			text=self.__get_text(),
			size_hint=(None, None),
			size=(30, 30),
			font_size=14,
			group='calendar',
			markup=True
		)

	def set_pressed_state(self) -> None:
		self.state = 'down'

	def __get_text(self) -> str:
		if self.date.month != datetime.now().month:
			return f'[color=202325]{self.date.day}[/color]'

		return str(self.date.day)

	def bind_date(self, bind_method):
		self.bind(on_press=bind_method)

	def is_active(self) -> bool:
		return self.state == 'down'

	def activate(self) -> None:
		self.background_color = [1, 0, 0, 1]

	def deactivate(self) -> None:
		self.background_color = [1, 1, 1, 1]


class CalendarField(BoxLayout):
	NOW_DATE = datetime.now()
	MONTH_DAYS = list(Calendar().itermonthdates(
		year=NOW_DATE.year, month=NOW_DATE.month
	))

	def __init__(self, title: str):
		self.title = title
		self.view_text = Config.LANG.get(self.title.title(), '[Неизвестно]')

		super().__init__()

		self.fill_calendar_table()

	def fill_calendar_table(self) -> None:
		container = self.ids.calendar_table

		for week_day in ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']:
			container.add_widget(Label(
				size_hint=(None, None),
				size=(30, 30),
				text=week_day
			))

		for day in self.MONTH_DAYS:
			container.add_widget(CalendarDate(day))

	def set_value(self, date: Union[datetime.date, None], radio_field: int=None) -> None:
		if date is None:
			return

		childrens = self.ids.calendar_table.children[::-1][7:]

		for children in childrens:
			if children.date == date.date():
				children.set_pressed_state()
				break

		if radio_field is not None:
			self.update_active_dates(radio_field)

	def get_value(self) -> datetime.date:
		childrens = self.ids.calendar_table.children[::-1][7:]

		for children in childrens:
			if children.is_active():
				return children.date

	def bind_all(self, on_press_method):
		childrens = self.ids.calendar_table.children[::-1][7:]

		for children in childrens:
			children.bind_date(on_press_method)

	def update_active_dates(self, type_: int) -> None:
		getattr(self, f'update_dates_{type_}')()

	def update_dates_0(self) -> None:
		# 5/2 Graph
		self.deactivate_all()
		childrens = self.ids.calendar_table.children[::-1][7:]

		for num, children in enumerate(childrens):
			if not children.date.isoweekday() in (6, 7):
				children.activate()

	def update_dates_1(self) -> None:
		# 1/3 Graph
		self.deactivate_all()
		childrens = self.ids.calendar_table.children[::-1][7:]
		selected_date = self.get_value()

		for num, children in enumerate(childrens):
			if (children.date - selected_date).days % 4 == 0:
				children.activate()

	def update_dates_2(self) -> None:
		childrens = self.ids.calendar_table.children[::-1][7:]
		selected_date = self.get_value()

		for children in childrens:
			children.activate()

	def deactivate_all(self) -> None:
		childrens = self.ids.calendar_table.children[::-1][7:]

		for children in childrens:
			children.deactivate()


class RadioItem(BoxLayout):
	def __init__(self, title: str):
		self.title = title

		super().__init__()

	def change_state(self) -> None:
		if self.ids.check_box.state == 'normal':
			self.ids.check_box.state = 'down'
		else:
			self.ids.check_box.state = 'normal'

	def get_value(self) -> bool:
		return self.ids.check_box.state == 'down'

	def bind_check_box(self, bind_method) -> None:
		self.ids.check_box.bind(on_press=bind_method)


class RadioField(BoxLayout):
	POINTS = {
		0: '5/2',
		1: '1/3',
		2: 'Всегда'
	}

	def __init__(self, title):
		self.title = title
		self.view_text = Config.LANG.get(self.title.title(), '[Неизвестно]')

		super().__init__()

		self.fill_radiobuttons()

	def set_value(self, active_point: int) -> None:
		print(f'Radio field get value={active_point}')
		if active_point is not None:
			childrens = self.children[::-1][1:]
			childrens[active_point].change_state()

	def get_value(self) -> Union[int, None]:
		childrens = self.children[::-1][1:]

		for num, children in enumerate(childrens):
			if children.get_value():
				return num

	def fill_radiobuttons(self):
		for point in range(3):
			field = RadioItem(self.POINTS[point])
			self.add_widget(field)

	def bind_all(self, on_press_method) -> None:
		childrens = self.children[::-1][1:]

		for children in childrens:
			children.bind_check_box(on_press_method)


class WorkGraph(BoxLayout):
	def __init__(self, title: str):
		self.title = title
		self.calendar_field = CalendarField(self.title)
		self.radio_field = RadioField(self.title)

		self.calendar_field.bind_all(self.update_active_dates)
		self.radio_field.bind_all(self.update_active_dates)

		super().__init__()

		self.add_widget(self.radio_field)
		self.add_widget(self.calendar_field)

	def set_value(self, db_row, key) -> None:
		self.calendar_field.set_value(db_row.work_day, db_row.work_type)
		self.radio_field.set_value(db_row.work_type)

	def get_value(self) -> dict:
		return {
			'work_type': self.radio_field.get_value(),
			'work_day': self.calendar_field.get_value()
		}

	def update_active_dates(self, instance) -> None:
		radio_value = self.radio_field.get_value()
		calendar_value = self.calendar_field.get_value()

		if (calendar_value is not None and radio_value == 1) or \
			radio_value in (0, 2):

			self.calendar_field.update_active_dates(radio_value)

		else:	self.calendar_field.deactivate_all()


class CheckBoxItem(BoxLayout):
	def __init__(self, db_row, group: str=None):
		self.db_row = db_row
		self.title = str(self.db_row)

		super().__init__()

		self.ids.check_box.group = group

	def activate(self) -> None:
		self.ids.check_box.state = 'down'

	def get_value(self) -> bool:
		return self.ids.check_box.state == 'down'


class _ToManyField(BoxLayout):
	def __init__(self, title: str, group: str=None):
		self.title_ = title
		self.to_create = f'create_{self.title_}'
		self.view_text = Config.LANG.get(self.title_.title(), '[Неизвестно]')
		self.group = group

		super().__init__()

		self.table = getattr(db_models, self.title_.title())
		self.fill_item_list()

	def fill_item_list(self) -> None:
		container = self.ids.item_list
		items = self.table.query.all()

		for item in items:
			container.add_widget(CheckBoxItem(item, group=self.group))


class ForeignKeyField(_ToManyField):
	def __init__(self, title: str):
		self.title = title
		super().__init__(title=self.title, group=f'group_{title}')

	def set_value(self, db_row, key: str) -> None:
		value = getattr(db_row, key)

	def get_value(self) -> Union[int, None]:
		childrens = self.ids.item_list.children

		for children in childrens:
			if children.get_value():
				return children.db_row.id


class ManyToManyField(_ToManyField):
	def __init__(self, title: str):
		self.title = title
		super().__init__(title=title[:-1])

	def set_value(self, db_row, key: str) -> None:
		value = getattr(db_row, key)
		childrens = self.ids.item_list.children

		for children in childrens:
			if children.db_row in value:
				children.activate()

	def get_value(self) -> list:
		result = InstrumentedList()
		childrens = self.ids.item_list.children

		for children in childrens:
			if children.get_value():
				item = self.table.query.filter_by(id=children.db_row.id)
				result.append(item.first())

		return result