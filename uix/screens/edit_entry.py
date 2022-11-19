from config import LOCALIZED
from data_base import db
from data_base import manager as DBManager
from uix import fields
from .create_entry import CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
	CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype


def get_id_from_list(foreign_key_field: fields.SelectedList) -> int:
	selected_element = foreign_key_field.get_value()

	return selected_element[0].id if selected_element else None


class EditEntryTag(CreateEntryTag):
	''' Экран редаектирования тега '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_tag'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.emergencies.set_value(self.element.emergencys)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'emergencys': self.emergencies.get_value()}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()

	def update_selected_lists(self) -> None:
		if self.element is None:
			return

		super().update_selected_lists()
		self.emergencies.set_value(self.element.emergencys)


class EditEntryRank(CreateEntryRank):
	''' Экран редаектирования звания '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_rank'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.humans.set_value(self.element.humans)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'humans': self.humans.get_value(),
		}
		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()

	def update_selected_lists(self) -> None:
		if self.element is None:
			return

		super().update_selected_lists()
		self.humans.set_value(self.element.humans)


class EditEntryPosition(CreateEntryPosition):
	''' Экран редаектирования должности '''

	def __init__(self, path_manager):
		super().__init__(path_manager)

		self.name = 'edit_position'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.humans.set_value(self.element.humans)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'humans': self.humans.get_value(),
		}
		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()

	def update_selected_lists(self) -> None:
		if self.element is None:
			return

		super().update_selected_lists()
		self.humans.set_value(self.element.humans)


class EditEntryHuman(CreateEntryHuman):
	''' Экран редаектирования человека '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_human'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.phone_1.set_value(self.element.phone_1)
		self.phone_2.set_value(self.element.phone_2)
		self.work_day.set_value(self.element.work_day)
		self.work_type.set_value(self.element.worktype)
		self.rank.set_value(self.element.rank)
		self.position.set_value(self.element.position)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'phone_1': self.phone_1.get_value(),
			'phone_2': self.phone_2.get_value(),
			'work_day': self.work_day.get_value(),
			'worktype': get_id_from_list(self.work_type),
			'rank': get_id_from_list(self.rank),
			'position': get_id_from_list(self.position)
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()

	def update_selected_lists(self) -> None:
		if self.element is None:
			return

		super().update_selected_lists()
		self.work_type.set_value(self.element.worktype)
		self.rank.set_value(self.element.rank)
		self.position.set_value(self.element.position)


class EditEntryEmergency(CreateEntryEmergency):
	''' Экран редаектирования ЧС '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_emergency'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.description.set_value(self.element.description)
		self.urgent.set_value(self.element.urgent)
		self.humans.set_value(self.element.humans)
		self.tags.set_value(self.element.tags)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'description': self.description.get_value(),
			'urgent': self.urgent.get_value(),
			'humans': self.humans.get_value(),
			'tags': self.tags.get_value()
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()

	def update_selected_lists(self) -> None:
		if self.element is None:
			return

		super().update_selected_lists()
		self.humans.set_value(self.element.humans)
		self.tags.set_value(self.element.tags)


class EditEntryWorktype(CreateEntryWorktype):
	''' Экран редаектирования графика работы '''

	def __init__(self, path_manager):
		super().__init__(path_manager)
		
		self.name = 'edit_worktype'
		self.toolbar.title = LOCALIZED.translate(self.name)
		self.element = None

	def set_element(self, element: db.Model) -> None:
		self.element = element

		self.fill_fields()

	def fill_fields(self) -> None:
		self.title.set_value(self.element.title)
		self.start_work_day.set_value(self.element.start_work_day)
		self.finish_work_day.set_value(self.element.finish_work_day)
		self.work_day_range.set_value(self.element.work_day_range)
		self.week_day_range.set_value(self.element.week_day_range)

	def insert(self) -> None:
		values = {
			'title': self.title.get_value(),
			'start_work_day': self.start_work_day.get_value(),
			'finish_work_day': self.finish_work_day.get_value(),
			'work_day_range': self.work_day_range.get_value(),
			'week_day_range': self.week_day_range.get_value()
		}

		successful_entry = DBManager.update(self.element, values)

		if successful_entry:
			self.path_manager.back()