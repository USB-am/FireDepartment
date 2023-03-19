import data_base

from . import create_model


class _BaseEditModelScreen:
	''' Базовое представление экрана редактирования '''

	def fill_content(self, entry: data_base.db.Model) -> None:
		raise AttributeError('Class _BaseEditModelScreen is hasn\'t "fill_content" method!')


class EditTagScreen(_BaseEditModelScreen, create_model.CreateTagScreen):
	''' Экран редактирования Тега '''

	name = 'edit_tag'
	table = data_base.Tag

	def fill_content(self, entry: data_base.Tag) -> None:
		self.title.set_value(entry.title)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=lambda e: print('Edit Tag')
		)


class EditRankScreen(_BaseEditModelScreen, create_model.CreateRankScreen):
	''' Экран редактирования Звания '''

	name = 'edit_rank'
	table = data_base.Rank

	def fill_content(self, entry: data_base.Rank) -> None:
		self.title.set_value(entry.title)
		self.priority.set_value(entry.priority)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=lambda e: print('Edit Rank')
		)


class EditPositionScreen(_BaseEditModelScreen, create_model.CreatePositionScreen):
	''' Экран редактирования Должности '''

	name = 'edit_position'
	table = data_base.Position

	def fill_content(self, entry: data_base.Position) -> None:
		self.title.set_value(entry.title)
		self.submit.text = 'Редактировать'
		self.submit.bind_btn(
			callback=lambda e: print('Edit Position')
		)


class EditHumanScreen(_BaseEditModelScreen, create_model.CreateHumanScreen):
	''' Экран редактирования Человека '''

	name = 'edit_human'
	table = data_base.Human

	def fill_content(self, entry: data_base.Human) -> None:
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
			callback=lambda e: print('Edit Human')
		)


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