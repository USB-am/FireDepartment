from sqlalchemy.orm.collections import InstrumentedList

import data_base
from app.path_manager import PathManager
from data_base import manager
from . import create_model
from ui.fields.submit import FDSubmit


class _BaseEditModelScreen:
	''' Базовое представление экрана редактирования '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self._entry = None

	def fill_content(self, entry: data_base.db.Model) -> None:
		raise AttributeError('Class _BaseEditModelScreen is hasn\'t "fill_content" method!')

	def save(self, instance: FDSubmit) -> None:
		update_status = self.update_entry()

		if update_status:
			self.path_manager.back()


class EditTagScreen(_BaseEditModelScreen, create_model.CreateTagScreen):
	''' Экран редактирования Тега '''

	name = 'edit_tag'
	table = data_base.Tag

	def fill_content(self, entry: data_base.Tag) -> None:
		self._entry = entry

		self.title.set_value(entry.title)
		self.emergencies.set_value(entry.emergencys)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=self.save
		)

	def update_entry(self) -> None:
		values = {
			'title': self.title.get_value(),
			'emergencys': self.emergencies.get_value()
		}
		request_status = manager.update(self._entry, **values)

		return request_status


class EditRankScreen(_BaseEditModelScreen, create_model.CreateRankScreen):
	''' Экран редактирования Звания '''

	name = 'edit_rank'
	table = data_base.Rank

	def fill_content(self, entry: data_base.Rank) -> None:
		self._entry = entry

		self.title.set_value(entry.title)
		self.priority.set_value(entry.priority)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=self.save
		)

	def update_entry(self) -> None:
		values = {
			'title': self.title.get_value(),
			'priority': self.priority.get_value(),
			'humans': self.humans.get_value()
		}
		request_status = manager.update(self._entry, **values)

		return request_status


class EditPositionScreen(_BaseEditModelScreen, create_model.CreatePositionScreen):
	''' Экран редактирования Должности '''

	name = 'edit_position'
	table = data_base.Position

	def fill_content(self, entry: data_base.Position) -> None:
		self._entry = entry

		self.title.set_value(entry.title)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=self.save
		)

	def update_entry(self) -> None:
		values = {
			'title': self.title.get_value(),
			'humans': self.humans.get_value(),
		}
		request_status = manager.update(self._entry, **values)

		return request_status


class EditHumanScreen(_BaseEditModelScreen, create_model.CreateHumanScreen):
	''' Экран редактирования Человека '''

	name = 'edit_human'
	table = data_base.Human

	def fill_content(self, entry: data_base.Human) -> None:
		self._entry = entry

		self.title.set_value(entry.title)
		self.phone_1.set_value(entry.phone_1)
		self.phone_2.set_value(entry.phone_2)
		self.is_firefigher.set_value(entry.is_firefigher)
		self.work_day.set_value(entry.work_day)
		self.worktype.set_value(entry.worktype)
		self.position.set_value(entry.position)
		self.rank.set_value(entry.rank)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=self.save
		)

	def update_entry(self) -> None:
		worktype_obj = self.worktype.get_value()[0] if self.worktype.get_value() else None
		position_obj = self.position.get_value()[0] if self.position.get_value() else None
		rank_obj = self.rank.get_value()[0] if self.rank.get_value() else None
		# worktype_obj = self.worktype.get_value()
		# position_obj = self.position.get_value()
		# rank_obj = self.rank.get_value()

		values = {
			'title': self.title.get_value(),
			'phone_1': self.phone_1.get_value(),
			'phone_2': self.phone_2.get_value(),
			'is_firefigher': self.is_firefigher.get_value(),
			'work_day': self.work_day.get_value(),
			'worktype': worktype_obj,
			'position': position_obj,
			'rank': rank_obj,
		}
		# for key, value in values.items():
		# 	print(f'{key}: {value} [{type(value)}]')
		# print('\n'*10)
		request_status = manager.update(self._entry, **values)

		return request_status


class EditEmergencyScreen(_BaseEditModelScreen, create_model.CreateEmergencyScreen):
	''' Экран редактирования Вызова '''

	name = 'edit_emergency'
	table = data_base.Emergency

	def fill_content(self, entry: data_base.Emergency) -> None:
		self.title.set_value(entry.title)
		self.description.set_value(entry.description)
		self.urgent.set_value(entry.urgent)
		self.humans.set_value(entry.humans)
		self.tags.set_value(entry.tags)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=lambda e: print('Edit Emergency')
		)