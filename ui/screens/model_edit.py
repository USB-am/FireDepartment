from . import model_create
from app.path_manager import PathManager
from data_base import Tag, Rank, Position, Human, Emergency, Worktype


class _BaseEditModel(model_create._BaseCreateModel):
	''' Базовое представление страницы редактирования записи '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.rem_right_button()
		self.ids.toolbar.add_right_button(
			icon='check',
			callback=lambda *_: print('Update entry button is pressed')
		)

		e = self.model.query.first()
		self.fill_fields(e)


class TagEditModel(_BaseEditModel, model_create.TagCreateModel):
	''' Страница редактирования записи из модели Tag '''

	name = 'edit_tag'
	model = Tag
	toolbar_title = 'Редактирование Тега'

	def fill_fields(self, entry: Tag) -> None:
		self.params['title'].set_value(entry.title)
		self.params['emergencys'].set_value(entry.emergencys)


class RankEditModel(_BaseEditModel, model_create.RankCreateModel):
	''' Страница редактирования записи из модели Rank '''

	name = 'edit_rank'
	model = Rank
	toolbar_title = 'Редактирование Звания'

	def fill_fields(self, entry: Rank) -> None:
		self.params['title'].set_value(entry.title)
		self.params['priority'].set_value(entry.priority)
		self.params['humans'].set_value(entry.humans)


class PositionEditModel(_BaseEditModel, model_create.PositionCreateModel):
	''' Страница редактирования записи из модели Position '''

	name = 'edit_position'
	model = Position
	toolbar_title = 'Редактирование Должности'

	def fill_fields(self, entry: Position) -> None:
		self.params['title'].set_value(entry.title)
		self.params['humans'].set_value(entry.humans)


class HumanEditModel(_BaseEditModel, model_create.HumanCreateModel):
	''' Страница редактирования записи из модели Human '''

	name = 'edit_human'
	model = Human
	toolbar_title = 'Редактирование Человека'

	def fill_fields(self, entry: Human) -> None:
		self.params['title'].set_value(entry.title)
		self.params['phone_1'].set_value(entry.phone_1)
		self.params['phone_2'].set_value(entry.phone_2)
		self.params['is_firefigher'].set_value(entry.is_firefigher)
		self.params['work_day'].set_value(entry.work_day)
		self.params['worktype'].set_value(entry.worktype)
		self.params['position'].set_value(entry.position)
		self.params['rank'].set_value(entry.rank)


class EmergencyEditModel(_BaseEditModel, model_create.EmergencyCreateModel):
	''' Страница редактирования записи из модели Emergency '''

	name = 'edit_emergency'
	model = Emergency
	toolbar_title = 'Редактирование Вызова'

	def fill_fields(self, entry: Emergency) -> None:
		self.params['title'].set_value(entry.title)
		self.params['description'].set_value(entry.description)
		self.params['urgent'].set_value(entry.urgent)
		self.params['tags'].set_value(entry.tags)
		self.params['humans'].set_value(entry.humans)


class WorktypeEditModel(_BaseEditModel, model_create.WorktypeCreateModel):
	''' Страница редактирования записи из модели Worktype '''

	name = 'edit_worktype'
	model = Worktype
	toolbar_title = 'Редактирование Графика работы'

	def fill_fields(self, entry: Worktype) -> None:
		self.params['title'].set_value(entry.title)
		self.params['start_work_day'].set_value(entry.start_work_day)
		self.params['finish_work_day'].set_value(entry.finish_work_day)
		self.params['work_day_range'].set_value(entry.work_day_range)
		self.params['week_day_range'].set_value(entry.week_day_range)
		self.params['humans'].set_value(entry.humans)
