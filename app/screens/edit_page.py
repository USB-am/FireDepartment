from collections import OrderedDict

from kivy.uix.button import Button

from config import path_manager
from data_base import db, Tag, Rank, Position, Human, Emergency, manager
from app.tools.custom_screen import CustomScrolledScreen
from app.tools.fields.label import FDEntry, FDTextArea
from app.tools.fields.selected_list import SelectedList
from app.tools.fields.controllers import FDSwitch


class BaseUpdateDBTable(CustomScrolledScreen):
	''' Базовый класс создания/изменения элемента базы данных '''
	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.back())

		self.__init_ui()

	def __init_ui(self) -> None:
		for key, field in self.fields.items():
			self.add_widgets(field)


class BaseCreatePage(BaseUpdateDBTable):
	''' Экран создания элемента базы данных '''
	def __init__(self):
		super().__init__()

		self.toolbar.add_right_button('check', lambda e: self.insert_values())

	def insert_values(self) -> None:
		rows_count = len(self.table.query.all())
		title = f'{self.table.__tablename__} #{rows_count+1}'

		manager.insert(self.table, {'title': title})
		self.back()


class BaseEditPage(BaseUpdateDBTable):
	''' Экран изменения элемента базы данных '''
	def __init__(self):
		super().__init__()

		self.toolbar.add_right_button('check', lambda e: \
			print('You pressed on submit button'))

	def _update_content(self, db_row: db.Model) -> None:
		for column_name, field in self.fields.items():
			field.set_value(getattr(db_row, column_name))


class EditTag(BaseEditPage):
	name = 'edit_tag'
	table = Tag

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class EditRank(BaseEditPage):
	name = 'edit_rank'
	table = Rank

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class EditPosition(BaseEditPage):
	name = 'edit_position'
	table = Position

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class EditHuman(BaseEditPage):
	name = 'edit_human'
	table = Human

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
			'phone_1': FDEntry('phone_1'),
			'phone_2': FDEntry('phone_2'),
			# 'work_day': FDCalendar('work_day'),
			# 'worktype': FDWorkType('worktype'),
			'position': SelectedList(Position.icon, 'Position', 'update_human', True),
			'rank': SelectedList(Rank.icon, 'Rank', 'update_rank', True),
		})

		super().__init__()


class EditEmergency(BaseEditPage):
	name = 'edit_emergency'
	table = Emergency

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
			'description': FDTextArea('description'),
			'urgent': FDSwitch('truck-fast', 'Urgent'),
			'humans': SelectedList(Human.icon, 'Humans', 'update_humans', True),
			'tags': SelectedList(Tag.icon, 'Tags', 'update_tags', True),
		})

		super().__init__()


class CreateTag(BaseCreatePage):
	name = 'create_tag'
	table = Tag

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class CreateRank(BaseCreatePage):
	name = 'create_rank'
	table = Rank

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class CreatePosition(BaseCreatePage):
	name = 'create_position'
	table = Position

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})

		super().__init__()


class CreateHuman(BaseCreatePage):
	name = 'create_human'
	table = Human

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
			'phone_1': FDEntry('phone_1'),
			'phone_2': FDEntry('phone_2'),
			# 'work_day': FDCalendar('work_day'),
			# 'worktype': FDWorkType('worktype'),
			'position': SelectedList(Position.icon, 'Position', 'update_human', True),
			'rank': SelectedList(Rank.icon, 'Rank', 'update_rank', True),
		})

		super().__init__()


class CreateEmergency(BaseCreatePage):
	name = 'create_emergency'
	table = Emergency

	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
			'description': FDTextArea('description'),
			'urgent': FDSwitch('truck-fast', 'Urgent'),
			'humans': SelectedList(Human.icon, 'Humans', 'update_humans', True),
			'tags': SelectedList(Tag.icon, 'Tags', 'update_tags', True),
		})

		super().__init__()