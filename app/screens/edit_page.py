from collections import OrderedDict

from config import LOCALIZED, path_manager
from data_base import db, Tag, Rank, Position, Human, Emergency
from app.tools.custom_screen import CustomScrolledScreen
from app.tools.fields.label import FDEntry, FDTextArea
from app.tools.fields.selected_list import SelectedList
from app.tools.fields.controllers import FDSwitch


class BaseUpdateTagTable:
	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})


class BaseUpdateRankTable:
	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})


class BaseUpdatePositionTable:
	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
		})


class BaseUpdateHumanTable:
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


class BaseUpdateEmergencyTable:
	def __init__(self):
		self.fields = OrderedDict({
			'title': FDEntry('title'),
			'description': FDTextArea('description'),
			'urgent': FDSwitch('truck-fast', 'Urgent'),
			'tags': SelectedList(Tag.icon, 'Tags', 'update_tags', True),
			'humans': SelectedList(Human.icon, 'Humans', 'update_humans', True),
		})


class BaseUpdateDBTable(CustomScrolledScreen):
	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())

		self.__init_ui()

	def __init_ui(self) -> None:
		for key, field in self.fields.items():
			self.add_widgets(field)
		# pass


class BaseEditPage(BaseUpdateDBTable):
	# def __init__(self):
	# 	super().__init__()

	# 	self.entry = FDEntry('Title')
	# 	self.add_widgets(self.entry)

	def _update_content(self, db_row: db.Model) -> None:
		pass


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