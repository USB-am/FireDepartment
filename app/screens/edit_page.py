from collections import OrderedDict

from config import LOCALIZED, path_manager
from data_base import db, Tag, Rank, Position, Human, Emergency
from app.tools.custom_screen import CustomScrolledScreen
from app.tools.fields.label import FDEntry, FDTextArea
from app.tools.fields.selected_list import SelectedList
from app.tools.fields.controllers import FDSwitch


class BaseUpdateTagTable:
	fields = OrderedDict({
		'title': FDEntry,#('title'),
	})


class BaseUpdateRankTable:
	fields = OrderedDict({
		'title': FDEntry,#('title'),
	})


class BaseUpdatePositionTable:
	fields = OrderedDict({
		'title': FDEntry,#('title'),
	})


class BaseUpdateHumanTable:
	fields = OrderedDict({
		'title': FDEntry,#('title'),
		'phone_1': FDEntry,#('phone_1'),
		'phone_2': FDEntry,#('phone_2'),
		# 'work_day': FDCalendar,#('work_day'),
		# 'worktype': FDWorkType,#('worktype'),
		'position': SelectedList,#(Position.icon, 'Position', 'update_human', True),
		'rank': SelectedList,#(Rank.icon, 'Rank', 'update_rank', True),
	})


class BaseUpdateEmergencyTable:
	fields = OrderedDict({
		'title': FDEntry,#('title'),
		'description': FDTextArea,#('description'),
		'urgent': FDSwitch,#('truck-fast', 'Urgent'),
		'tags': SelectedList,#(Tag.icon, 'Tags', 'update_tags', True),
		'humans': SelectedList,#(Human.icon, 'Humans', 'update_humans', True),
	})


class BaseUpdateDBTable(CustomScrolledScreen):
	def __init__(self):
		super().__init__()

		self.toolbar.add_left_button('arrow-left', lambda e: \
			self.path_manager_.back())

		self.__init_ui()

	def __init_ui(self) -> None:
		pass


class BaseEditPage(BaseUpdateDBTable):
	def __init__(self):
		super().__init__()

		self.entry = FDEntry('Title')
		self.add_widgets(self.entry)

	def _update_content(self, db_row: db.Model) -> None:
		pass


class EditTag(BaseUpdateTagTable, BaseEditPage):
	name = 'edit_tag'
	table = Tag


class EditRank(BaseUpdateRankTable, BaseEditPage):
	name = 'edit_rank'
	table = Rank


class EditPosition(BaseUpdatePositionTable, BaseEditPage):
	name = 'edit_position'
	table = Position


class EditHuman(BaseUpdateHumanTable, BaseEditPage):
	name = 'edit_human'
	table = Human


class EditEmergency(BaseUpdateEmergencyTable, BaseEditPage):
	name = 'edit_emergency'
	table = Emergency