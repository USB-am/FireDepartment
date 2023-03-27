from app.path_manager import PathManager
import data_base
from data_base import manager
from . import BaseScrolledScreen
from ui.fields.entry import FDTextInput, FDNumInput, FDDescriptionInput
from ui.fields.select_list import FDSelectList
from ui.fields.submit import FDSubmit
from ui.fields.switch import FDSwitch, FDStatusSwitch
from ui.fields.date import FDDate, FDDateTime


class _BaseCreateModelScreen(BaseScrolledScreen):
	''' Базовое представление экрана создания '''

	def __init__(self, path_manager: PathManager):
		self.path_manager = path_manager

		super().__init__()

		self.__fill_toolbar()

		self.bind(on_pre_enter=lambda *e: self.pre_enter())

	def pre_enter(self) -> None:
		self.clear()
		self._fill_content()
		self.update()

	def __fill_toolbar(self) -> None:
		self.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda e: self.path_manager.back()
		)

	def update(self) -> None:
		pass


class CreateTagScreen(_BaseCreateModelScreen):
	''' Экран создания тега '''

	name = 'create_tag'
	table = data_base.Tag

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.emergencies = FDSelectList(
			icon=self.table.icon,
			title='Вызовы'
		)
		self.emergencies.add_right_button(
			callback=lambda e: self.path_manager.forward('create_emergency')
		)
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(
			callback=lambda e: self.insert()
		)

		self.add_widgets(self.title, self.emergencies, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'emergencys': self.emergencies.get_value()
		}
		request_status = manager.insert(self.table, **values)

		print(f'insert is {request_status}')

	def update(self) -> None:
		self.emergencies.add(*data_base.Emergency.query.all())


class CreateRankScreen(_BaseCreateModelScreen):
	''' Экран создания Звания '''

	name = 'create_rank'
	table = data_base.Rank

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.priority = FDNumInput(hint_text='Приоритетность')
		self.humans = FDSelectList(
			icon=data_base.Human.icon,
			title='Люди'
		)
		self.humans.add_right_button(
			callback=lambda e: self.path_manager.forward('create_human')
		)
		self.humans.add(*data_base.Human.query.all())
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(callback=lambda e: self.insert())

		self.add_widgets(self.title, self.priority, self.humans, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'priority': self.priority.get_value(),
			# 'humans': self.humans.get_value(),
		}
		request_status = manager.insert(self.table, **values)

		print(f'CreateRankScreen.insert is {request_status}')


class CreatePositionScreen(_BaseCreateModelScreen):
	''' Экран создания Должности '''

	name = 'create_position'
	table = data_base.Position

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.humans = FDSelectList(
			icon=data_base.Human.icon,
			title='Люди'
		)
		self.humans.add_right_button(
			callback=lambda e: self.path_manager.forward('create_human')
		)
		self.humans.add(*data_base.Human.query.all())
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(callback=lambda e: self.insert())

		self.add_widgets(self.title, self.humans, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			# 'humans': self.humans.get_value(),
		}
		request_status = manager.insert(self.table, **values)

		print(f'CreatePositionScreen.insert is {request_status}')


class CreateHumanScreen(_BaseCreateModelScreen):
	''' Экран создания Человека '''

	name = 'create_human'
	table = data_base.Human

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='ФИО')
		self.phone_1 = FDTextInput(hint_text='Телефон')
		self.phone_2 = FDTextInput(hint_text='Дополнительный телефон')
		self.is_firefigher = FDStatusSwitch(
			active_icon='fire-truck',
			active_title='Пожарный',
			deactive_icon='card-account-phone',
			deactive_title='Контакт'
		)
		self.work_day = FDDate(icon='calendar-month', title='Рабочий день')
		self.worktype = FDSelectList(
			icon=data_base.Worktype.icon,
			title='График работы'
		)
		self.worktype.add_right_button(
			callback=lambda e: self.path_manager.forward('create_worktype')
		)
		self.worktype.add(*data_base.Worktype.query.all())
		self.position = FDSelectList(
			icon=data_base.Position.icon,
			title='Должжность'
		)
		self.position.add_right_button(
			callback=lambda e: self.path_manager.forward('create_position')
		)
		self.position.add(*data_base.Position.query.all())
		self.rank = FDSelectList(
			icon=data_base.Rank.icon,
			title='Звание'
		)
		self.rank.add_right_button(
			callback=lambda e: self.path_manager.forward('create_rank')
		)
		self.rank.add(*data_base.Rank.query.all())
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(callback=lambda e: self.insert())

		self.add_widgets(self.title, self.phone_1, self.phone_2,
			self.is_firefigher, self.work_day, self.worktype, self.position,
			self.rank, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'phone_1': self.phone_1.get_value(),
			'phone_2': self.phone_2.get_value(),
			'is_firefigher': self.is_firefigher.get_value(),
			'work_day': self.work_day.get_value(),
			'worktype': self.worktype.get_value(),
			'position': self.position.get_value(),
			'rank': self.rank.get_value(),
		}
		input(f'work day type is {type(values["work_day"])}')
		request_status = manager.insert(self.table, **values)

		print(f'CreateHumanScreen.insert is {request_status}')


class CreateEmergencyScreen(_BaseCreateModelScreen):
	''' Экран создания Вызова '''

	name = 'create_emergency'
	table = data_base.Emergency

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.description = FDDescriptionInput(hint_text='Описание')
		self.urgent = FDSwitch(icon='truck-fast', title='Срочный')
		self.humans = FDSelectList(
			icon=data_base.Human.icon,
			title='Люди'
		)
		self.humans.add_right_button(
			callback=lambda e: self.path_manager.forward('create_human')
		)
		self.humans.add(*data_base.Human.query.all())
		self.tags = FDSelectList(
			icon=data_base.Tag.icon,
			title='Теги'
		)
		self.tags.add_right_button(
			callback=lambda e: self.path_manager.forward('create_tag')
		)
		self.tags.add(*data_base.Tag.query.all())
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(callback=lambda e: self.insert())

		self.add_widgets(self.title, self.description, self.urgent,
			self.humans, self.tags, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'description': self.description.get_value(),
			'urgent': self.urgent.get_value(),
			'humans': self.humans.get_value(),
			'tags': self.tags.get_value()
		}
		request_status = manager.insert(self.table, **values)

		print(f'CreateEmergencyScreen.insert is {request_status}')


class CreateWorktypeScreen(_BaseCreateModelScreen):
	''' Экран создания Графика работы '''

	name = 'create_worktype'
	table = data_base.Worktype

	def _fill_content(self) -> None:
		self.title = FDTextInput(hint_text='Название')
		self.start_work_day = FDDateTime(
			icon='run-fast',
			title='Начало рабочего дня'
		)
		self.finish_work_day = FDDateTime(
			icon='exit-run',
			title='Конец рабочего дня'
		)
		self.work_day_range = FDNumInput(hint_text='Количество рабочих дней')
		self.week_day_range = FDNumInput(hint_text='Количество выходных дней')
		self.submit = FDSubmit(text='Создать')
		self.submit.bind_btn(callback=lambda e: self.insert())

		self.add_widgets(self.title, self.start_work_day, self.finish_work_day,
			self.work_day_range, self.week_day_range, self.submit)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'start_work_day': self.start_work_day.get_value(),
			'finish_work_day': self.finish_work_day.get_value(),
			'work_day_range': self.work_day_range.get_value(),
			'week_day_range': self.week_day_range.get_value(),
		}
		request_status = manager.insert(self.table, **values)

		print(f'CreateWorktypeScreen.insert is {request_status}')