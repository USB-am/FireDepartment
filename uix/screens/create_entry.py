from custom_screen import CustomScrolledScreen
from config import LOCALIZED
from uix import fields
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype


class CreateEntry(CustomScrolledScreen):
	''' Базовый экран создания новой записи в базе данных '''

	def __init__(self, path_manager, table: db.Model):
		super().__init__()

		self.name = f'create_{table.__tablename__}'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Create {self.table.__tablename__}')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('plus', lambda e: self.insert())

	def insert(self) -> None:
		pass


class CreateEntryTag(CreateEntry):
	''' Экран создания новой записи в таблицу Tag '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Tag)

		self.title = fields.StringField(
			title='Title',
			help_text='Название тега.\n\nДолжно быть уникальным т.к. поиск будет производиться именно по этому полю.'
		)
		self.emergencies = fields.SelectedList(
			icon=Emergency.icon,
			title=Emergency.__tablename__,
			values=Emergency.query.all())
		self.emergencies.binding(path_manager)

		self.add_widgets(self.title, self.emergencies)

	def insert(self) -> None:
		tag = Tag(
			title=self.title.get_value(),
			emergencys=self.emergencies.get_value())
		db.session.add(tag)
		db.session.commit()

		self.path_manager.back()


class CreateEntryRank(CreateEntry):
	''' Экран создания новой записи в таблицу Rank '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Rank)

		self.title = fields.StringField(
			title='Title',
			help_text='Название звания.\n\nДолжно быть уникальным т.к. поиск будет производиться именно по этому полю.'
		)
		self.humans = fields.SelectedList(
			icon=Human.icon,
			title=Human.__tablename__,
			values=Human.query.all())
		self.humans.binding(path_manager)

		self.add_widgets(self.title, self.humans)

	def insert(self) -> None:
		rank = Rank(title=self.title.get_value())

		db.session.add(rank)
		db.session.commit()

		self.path_manager.back()


class CreateEntryPosition(CreateEntry):
	''' Экран создания новой записи в таблицу Position '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Position)

		self.title = fields.StringField(
			title='Title',
			help_text='Название должности.\n\nДолжно быть уникальным т.к. поиск будет производиться именно по этому полю.'
		)
		self.humans = fields.SelectedList(
			icon=Human.icon,
			title=Human.__tablename__,
			values=Human.query.all())
		self.humans.binding(path_manager)

		self.add_widgets(self.title, self.humans)

	def insert(self) -> None:
		position = Position(title=self.title.get_value())

		db.session.add(position)
		db.session.commit()

		self.path_manager.back()


class CreateEntryHuman(CreateEntry):
	''' Экран создания новой записи в таблицу Human '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Human)

		self.title = fields.StringField(
			title='Title',
			help_text='Название тела.\n\n(!) Поле не может быть пустым.')
		self.phone_1 = fields.PhoneField('Phone')
		self.phone_2 = fields.PhoneField('Addition phone')
		self.work_day = fields.DateField('calendar-month', 'Work day')
		self.work_type = fields.SelectedList(
			icon=Worktype.icon,
			title=Worktype.__tablename__,
			values=Worktype.query.all(),
			group='worktypes')
		self.rank = fields.SelectedList(
			icon=Rank.icon,
			title=Rank.__tablename__,
			values=Rank.query.all(),
			group='ranks')
		self.position = fields.SelectedList(
			icon=Position.icon,
			title=Position.__tablename__,
			values=Position.query.all(),
			group='positions')

		self.work_type.binding(path_manager)
		self.rank.binding(path_manager)
		self.position.binding(path_manager)

		self.add_widgets(self.title, self.phone_1, self.phone_2, self.work_day,
		                 self.work_type, self.rank, self.position)

	def insert(self) -> None:
		human = Human(
			title=self.title.get_value(),
			phone_1=self.phone_1.get_value(),
			phone_2=self.phone_2.get_value(),
			work_day=self.work_day.get_value(),
			worktype=get_id_from_list(self.work_type),
			position=get_id_from_list(self.position),
			rank=get_id_from_list(self.rank))

		db.session.add(human)
		db.session.commit()

		self.path_manager.back()


class CreateEntryEmergency(CreateEntry):
	''' Экран создания новой записи в таблицу Emergency '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Emergency)

		self.title = fields.StringField(
			title='Title',
			help_text='Название события.\n\n(!) Поле не может быть пустым.'
		)
		self.description = fields.DescriptionField('Description')
		self.urgent = fields.BooleanField('truck-fast', 'Urgent')
		self.humans = fields.SelectedList(
			icon=Human.icon,
			title=Human.__tablename__,
			values=Human.query.all())
		self.tags = fields.SelectedList(
			icon=Tag.icon,
			title=Tag.__tablename__,
			values=Tag.query.all())
		self.humans.binding(path_manager)
		self.tags.binding(path_manager)

		self.add_widgets(self.title, self.description, self.urgent, self.humans,
		                 self.tags)

	def insert(self) -> None:
		emergency = Emergency(
			title=self.title.get_value(),
			description=self.description.get_value(),
			urgent=self.urgent.get_value(),
			humans=self.humans.get_value(),
			tags=self.tags.get_value())

		db.session.add(emergency)
		db.session.commit()

		self.path_manager.back()


class CreateEntryWorktype(CreateEntry):
	''' Экран создания новой записи в таблицу Worktype '''

	def __init__(self, path_manager):
		super().__init__(path_manager, Worktype)

		self.title = fields.StringField('Title')
		self.start_work_day = fields.DateTimeField('run-fast', 'Start work day',
			'Дата и время начала рабочего дня')
		self.finish_work_day = fields.DateTimeField('exit-run', 'Finish work day',
			'Дата и время конца рабочего дня')
		self.work_day_range = fields.IntegerField('Work day range')
		self.week_day_range = fields.IntegerField('Week day range')

		self.add_widgets(self.title, self.start_work_day, self.finish_work_day,
		                 self.work_day_range, self.week_day_range)

	def insert(self) -> None:
		worktype = Worktype(
			title=self.title.get_value(),
			start_work_day=self.start_work_day.get_value(),
			finish_work_day=self.finish_work_day.get_value(),
			work_day_range=self.work_day_range.get_value(),
			week_day_range=self.week_day_range.get_value())
		db.session.add(worktype)
		db.session.commit()

		self.path_manager.back()