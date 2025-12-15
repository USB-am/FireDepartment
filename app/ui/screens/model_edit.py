from typing import Dict, Any

from kivy.uix.widget import Widget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from .base import model_create
from app.path_manager import PathManager
from ui.field.button import FDRectangleButton
from data_base.model import db, Tag, Rank, Position, Human, Emergency, Worktype, Short
from data_base.manager import update_entry, delete_entry, get_by_id
from validators.create_model_validators import EmptyValidator, UniqueExcludingValidator, \
	ZeroValidator


class _BaseEditModel(model_create._BaseCreateModel):
	''' Базовое представление страницы редактирования записи '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.rem_right_button()
		self.ids.toolbar.add_right_button(
			icon='check',
			callback=lambda *_: self.update_and_back()
		)

		delete_btn = FDRectangleButton(title='Удалить')
		delete_btn.bind_btn(callback=lambda *_: self.delete_and_back())
		self.add_content(delete_btn)

	def update_and_back(self) -> None:
		''' Обновить запись и вернуться на страницу назад '''

		model_params = {key: widget.get_value() \
			for key, widget in self.params.items()}
		confirmed = self.is_valid(model_params)

		if not confirmed:
			self.save(model_params)
			self.clear_form()
			back_screen = self._path_manager.back()
			if hasattr(back_screen, 'update_elements'):
				back_screen.update_elements()
		else:
			ok_btn = MDRaisedButton(text='Ок')
			dialog = MDDialog(
				title='Ошибка',
				text=confirmed[0].text,
				buttons=[ok_btn,]
			)
			ok_btn.bind(on_release=lambda *_: dialog.dismiss())

			dialog.open()

	def delete_and_back(self) -> None:
		''' Удалить запись и вернуться на страницу назад '''

		self.delete_()
		self.clear_form()
		back_screen = self._path_manager.back()
		if hasattr(back_screen, 'update_elements'):
			back_screen.update_elements()

	def save(self, params: Dict[str, Any]) -> None:
		''' Обновить данные в БД '''

		update_entry(self.entry, params)

	def delete_(self) -> None:
		''' Удалить запись '''

		delete_entry(self.entry)


class TagEditModel(_BaseEditModel, model_create.TagCreateModel):
	''' Страница редактирования записи из модели Tag '''

	name = 'edit_tag'
	model = Tag
	toolbar_title = 'Редактирование Тега'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Tag, 'title', self.entry),
			EmptyValidator(Tag, 'title')
		]

	def fill_fields(self, entry: Tag) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['emergencys'].set_value(entry.emergencys)

	def is_valid(self, params: Dict[str, Any]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class ShortEditModel(_BaseEditModel, model_create.ShortCreateModel):
	''' Страница редактирования записи из модели Short '''

	name = 'edit_short'
	model = Short
	toolbar_title = 'Редактирование Сокращения'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Short, 'title', self.entry),
			EmptyValidator(None, None)
		]

	def fill_fields(self, entry: Short) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['explanation'].set_value(entry.explanation)
		self.params['into_new_line'].set_value(entry.into_new_line)

	def is_valid(self, params: Dict[str, Any]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class RankEditModel(_BaseEditModel, model_create.RankCreateModel):
	''' Страница редактирования записи из модели Rank '''

	name = 'edit_rank'
	model = Rank
	toolbar_title = 'Редактирование Звания'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Rank, 'title', self.entry),
			EmptyValidator(None, None)
		]

	def fill_fields(self, entry: Rank) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['priority'].set_value(entry.priority)
		self.params['humans'].set_value(entry.humans)

	def is_valid(self, params: Dict[str, Any]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title']),
			EmptyValidator(self.model, 'priority')(
				text='Поле "Приоритет" не может быть пустым',
				value=params['priority'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class PositionEditModel(_BaseEditModel, model_create.PositionCreateModel):
	''' Страница редактирования записи из модели Position '''

	name = 'edit_position'
	model = Position
	toolbar_title = 'Редактирование Должности'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Position, 'title', self.entry),
			EmptyValidator(None, None)
		]

	def fill_fields(self, entry: Position) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['humans'].set_value(entry.humans)

	def is_valid(self, params: Dict[str, Any]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title']),
		)

		return tuple(filter(lambda check: not check.status, checks))


class HumanEditModel(_BaseEditModel, model_create.HumanCreateModel):
	''' Страница редактирования записи из модели Human '''

	name = 'edit_human'
	model = Human
	toolbar_title = 'Редактирование Человека'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Human, 'title', self.entry),
			EmptyValidator(None, None),
		]

	def fill_fields(self, entry: Human) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['phone_1'].set_value(entry.phone_1)
		self.params['phone_2'].set_value(entry.phone_2)
		self.params['is_firefigher'].set_value(entry.is_firefigher)
		self.params['work_day'].set_value(entry.work_day)
		self.params['start_vacation'].set_value(entry.start_vacation)
		self.params['finish_vacation'].set_value(entry.finish_vacation)
		self.params['worktype'].set_value(entry.worktype)
		self.params['position'].set_value(entry.position)
		self.params['rank'].set_value(entry.rank)
		self.calendar_field.select_work_days(
			work_day=self.work_date_field.get_value(),
			worktype=get_by_id(Worktype, self.worktype_field.get_value()),
			vacation=(self.start_vacation_field.get_value(),
			          self.finish_vacation_field.get_value())
		)

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "ФИО" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "ФИО" должно быть уникальным',
				value=params['title']),
		)

		return tuple(filter(lambda check: not check.status, checks))


class EmergencyEditModel(_BaseEditModel, model_create.EmergencyCreateModel):
	''' Страница редактирования записи из модели Emergency '''

	name = 'edit_emergency'
	model = Emergency
	toolbar_title = 'Редактирование Вызова'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Emergency, 'title', self.entry),
			EmptyValidator(None, None)
		]

	def fill_fields(self, entry: Emergency) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['description'].set_value(entry.description)
		self.params['urgent'].set_value(entry.urgent)
		self.params['tags'].set_value(entry.tags)
		self.params['humans'].set_value(entry.humans)

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']
			),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title']
			),
		)

		return tuple(filter(lambda check: not check.status, checks))


class WorktypeEditModel(_BaseEditModel, model_create.WorktypeCreateModel):
	''' Страница редактирования записи из модели Worktype '''

	name = 'edit_worktype'
	model = Worktype
	toolbar_title = 'Редактирование Графика работы'
	entry: db.Model = None

	def update_inputs_validators(self) -> None:
		self.title_field.validators = [
			UniqueExcludingValidator(Worktype, 'title', self.entry),
			EmptyValidator(None, None)
		]

	def fill_fields(self, entry: Worktype) -> None:
		self.entry = entry
		self.update_inputs_validators()
		self.params['title'].set_value(entry.title)
		self.params['start_work_day'].set_value(entry.start_work_day)
		self.params['finish_work_day'].set_value(entry.finish_work_day)
		self.params['work_day_range'].set_value(entry.work_day_range)
		self.params['week_day_range'].set_value(entry.week_day_range)
		self.params['humans'].set_value(entry.humans)

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueExcludingValidator(self.model, 'title', self.entry)(
				text='Поле "Название" должно быть уникальным',
				value=params['title']),
			EmptyValidator(self.model, 'start_work_day')(
				text='Поле "Начало рабочего дня" не может быть пустым',
				value=params['start_work_day']),
			EmptyValidator(self.model, 'finish_work_day')(
				text='Поле "Конец рабочего дня" не может быть пустым',
				value=params['finish_work_day']),
			EmptyValidator(self.model, 'work_day_range')(
				text='Поле "Рабочие дни подряд" не может быть пустым',
				value=params['work_day_range']),
			ZeroValidator(self.model, 'work_day_range')(
				text='Поле "Рабочие дни подряд" должно быть больше 0',
				value=params['work_day_range']),
			EmptyValidator(self.model, 'week_day_range')(
				text='Поле "Выходные дни подряд" не может быть пустым',
				value=params['week_day_range']),
		)

		return tuple(filter(lambda check: not check.status, checks))
