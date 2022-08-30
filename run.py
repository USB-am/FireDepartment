# -*- coding: utf-8 -*-

from kivy.config import Config
Config.set('graphics', 'width', '350')


from typing import Union

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from custom_screen import CustomScreen, CustomScrolledScreen
from config import LOCALIZED
from uix import FDSearchBlock, FDExpansionPanel, \
	ExpansionEmergencyElement, ExpansionOptionsElement, FDNoteBook, FDEmergencyTab, \
	ExpansionEditListElement, fields
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype


db.create_all()


class PathManager:
	''' Менеджер путей перехода '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager

		self.path = ['main_page', ]

	def forward(self, screen_name: str) -> Union[CustomScreen, CustomScrolledScreen]:
		self.__screen_manager.current = screen_name
		self.path.append(screen_name)

		return self.__screen_manager.current_screen

	def back(self) -> Union[CustomScreen, CustomScrolledScreen]:
		if len(self.path) > 1:
			self.path.pop(-1)

		self.__screen_manager.current = self.path[-1]

		return self.__screen_manager.current_screen


class MainPage(CustomScrolledScreen):
	''' Главный экран '''

	name = 'main_page'

	def __init__(self, path_manager: PathManager):
		self.search_block = FDSearchBlock()

		super().__init__(self.search_block)

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Main')
		self.toolbar.add_left_button('fire-truck',
			lambda e: self.path_manager.forward('current_calls'))
		self.toolbar.add_right_button('cog',
			lambda e: self.path_manager.forward('options'))

	def fill_content(self) -> None:
		for emergency in Emergency.query.all():
			element = FDExpansionPanel(emergency, ExpansionEmergencyElement)
			self.add_widgets(element)


class CurrentCalls(CustomScreen):
	''' Экран текущих вызовов '''

	name = 'current_calls'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Current calls')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('check-outline', lambda e: print('Done'))

	def fill_content(self) -> None:
		self.notebook = FDNoteBook()
		self.add_widgets(self.notebook)

	def add_tab(self, element: db.Model) -> None:
		self.notebook.add_widget(FDEmergencyTab(element))


class Options(CustomScrolledScreen):
	''' Экран настроек '''

	name = 'options'

	def __init__(self, path_manager: PathManager):
		super().__init__()

		self.path_manager = path_manager

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate('Options')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		for data_base_table in (Tag, Rank, Position, Human, Emergency, Worktype):
			element = FDExpansionPanel(data_base_table, ExpansionOptionsElement)
			element.content.binding(self.path_manager)
			self.add_widgets(element)


class CreateEntry(CustomScrolledScreen):
	''' Базовый экран создания новой записи в базе данных '''

	def __init__(self, path_manager: PathManager, table: db.Model):
		super().__init__()

		self.name = f'create_{table.__tablename__}'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Create {self.table.__tablename__}')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())
		self.toolbar.add_right_button('plus', lambda e: print('You pressed on "plus"'))


class CreateEntryTag(CreateEntry):
	''' Экран создания новой записи в таблицу Tag '''

	def __init__(self, path_manager: PathManager):
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

		self.add_widgets(self.title)
		self.add_widgets(self.emergencies)


class CreateEntryRank(CreateEntry):
	''' Экран создания новой записи в таблицу Rank '''

	def __init__(self, path_manager: PathManager):
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

		self.add_widgets(self.title)
		self.add_widgets(self.humans)


class CreateEntryPosition(CreateEntry):
	''' Экран создания новой записи в таблицу Position '''

	def __init__(self, path_manager: PathManager):
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

		self.add_widgets(self.title)
		self.add_widgets(self.humans)


class CreateEntryHuman(CreateEntry):
	''' Экран создания новой записи в таблицу Human '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager, Human)

		self.title = fields.StringField(
			title='Title',
			help_text='Название тела.\n\n(!) Поле не может быть пустым.'
		)
		self.phone_1 = fields.PhoneField('Phone')
		self.phone_2 = fields.PhoneField('Addition phone')
		self.work_day = fields.DateField('calendar-month', 'Work day')
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
		self.rank.binding(path_manager)
		self.position.binding(path_manager)

		self.add_widgets(self.title)
		self.add_widgets(self.phone_1)
		self.add_widgets(self.phone_2)
		self.add_widgets(self.work_day)
		self.add_widgets(self.rank)
		self.add_widgets(self.position)


class CreateEntryEmergency(CreateEntry):
	''' Экран создания новой записи в таблицу Emergency '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager, Emergency)

		self.title = fields.StringField(
			title='Title',
			help_text='Название события.\n\n(!) Поле не может быть пустым.'
		)
		self.decription = fields.DescriptionField('Description')
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

		self.add_widgets(self.title)
		self.add_widgets(self.decription)
		self.add_widgets(self.urgent)
		self.add_widgets(self.humans)
		self.add_widgets(self.tags)


class CreateEntryWorktype(CreateEntry):
	''' Экран создания новой записи в таблицу Worktype '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager, Worktype)

		self.title = fields.StringField('Title')
		self.start_work_day = fields.DateTimeField('run-fast', 'Start work day',
			'Дата и время начала рабочего дня')
		self.finish_work_day = fields.DateTimeField('exit-run', 'Finish work day',
			'Дата и время конца рабочего дня')
		self.work_day_range = fields.IntegerField('Work day range')
		self.week_day_range = fields.IntegerField('Week day range')

		self.add_widgets(self.title)
		self.add_widgets(self.start_work_day)
		self.add_widgets(self.finish_work_day)
		self.add_widgets(self.work_day_range)
		self.add_widgets(self.week_day_range)


class EditEntryList(CustomScrolledScreen):
	''' Базовый класс со списком редактируемых элементов базы данных '''

	def __init__(self, path_manager: PathManager, table: db.Model):
		super().__init__()

		self.name = f'edit_{table.__tablename__}_list'.lower()
		self.path_manager = path_manager
		self.table = table

		self.setup()
		self.fill_content()

	def setup(self) -> None:
		self.toolbar.title = LOCALIZED.translate(f'Edit {self.name} list')
		self.toolbar.add_left_button('arrow-left', lambda e: self.path_manager.back())

	def fill_content(self) -> None:
		for db_entry in self.table.query.all():
			element = ExpansionEditListElement(db_entry)
			element.binding(self.path_manager)
			self.add_widgets(element)


class EditEntryTag(CreateEntryTag):
	''' Экран редаектирования тега '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_tag'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class EditEntryRank(CreateEntryRank):
	''' Экран редаектирования звания '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_rank'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class EditEntryPosition(CreateEntryPosition):
	''' Экран редаектирования должности '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_position'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class EditEntryHuman(CreateEntryHuman):
	''' Экран редаектирования человека '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_human'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class EditEntryEmergency(CreateEntryEmergency):
	''' Экран редаектирования ЧС '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_emergency'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class EditEntryWorktype(CreateEntryTag):
	''' Экран редаектирования графика работы '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		
		self.name = 'edit_worktype'
		self.element = None

	def fill_fields(self, element: db.Model) -> None:
		self.element = element


class Application(MDApp):
	''' Главный класс приложения '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.path_manager = PathManager(self.screen_manager)

		self.setup()

		self.screen_manager.current = 'options'

	def setup(self) -> None:
		self.main_page = MainPage(self.path_manager)
		self.current_calls = CurrentCalls(self.path_manager)
		self.options = Options(self.path_manager)

		# Create screens
		for screen in (CreateEntryTag, CreateEntryRank, CreateEntryPosition, \
		               CreateEntryHuman, CreateEntryEmergency, CreateEntryWorktype):
			self.screen_manager.add_widget(screen(self.path_manager))

		# Edit screens_list
		self.edit_tag_list = EditEntryList(self.path_manager, Tag)
		self.edit_rank_list = EditEntryList(self.path_manager, Rank)
		self.edit_position_list = EditEntryList(self.path_manager, Position)
		self.edit_human_list = EditEntryList(self.path_manager, Human)
		self.edit_emergency_list = EditEntryList(self.path_manager, Emergency)
		self.edit_worktype_list = EditEntryList(self.path_manager, Worktype)

		self.screen_manager.add_widget(self.main_page)
		self.screen_manager.add_widget(self.current_calls)
		self.screen_manager.add_widget(self.options)

		self.screen_manager.add_widget(self.edit_tag_list)
		self.screen_manager.add_widget(self.edit_rank_list)
		self.screen_manager.add_widget(self.edit_position_list)
		self.screen_manager.add_widget(self.edit_human_list)
		self.screen_manager.add_widget(self.edit_emergency_list)
		self.screen_manager.add_widget(self.edit_worktype_list)

		# Edit screens
		for screen in (EditEntryTag, EditEntryRank, EditEntryPosition, \
		               EditEntryHuman, EditEntryEmergency, EditEntryWorktype):
			self.screen_manager.add_widget(screen(self.path_manager))

	def build(self) -> ScreenManager:
		return self.screen_manager


def main():
	app = Application()
	app.run()


if __name__ == '__main__':
	main()