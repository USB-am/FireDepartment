from typing import Dict

from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype, Short
from data_base.manager import write_entry, get_by_id
from ui.field.input import FDInput, FDMultilineInput, FDNumberInput, \
	FDPhoneInput
from ui.field.select import FDSelect, FDMultiSelect
from ui.field.switch import FDSwitch, FDDoubleSwitch
from ui.field.date import FDDate, FDDateTime
from ui.field.calendar import FDCalendar
from ui.field.button import FDButton
from ui.layout.dialogs import HumanDialogContent, EmergencyDialogContent, \
	WorktypeDialogContent, TagDialogContent, RankDialogContent, \
	PositionDialogContent, ShortDialogContent
from validators.create_model_validators import UniqueValidator, EmptyValidator, \
	ZeroValidator


class _BaseCreateModel(BaseScrollScreen):
	''' Базовое представление страницы создания записи в БД '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)

		self.ids.toolbar.add_left_button(
			icon='arrow-left',
			callback=lambda *_: self._path_manager.back()
		)
		self.ids.toolbar.add_right_button(
			icon='check',
			callback=lambda *_: self.save_and_back()
		)

		# Если значение == False, в методе _pre_open_update инициализирует
		# необходимые виджеты и переводит значение в True.
		self.was_opened = False
		self.params: Dict[str, Widget] = {}
		self.bind(on_pre_enter=lambda e: self._pre_open_update())

	def fill_elements(self) -> None:
		pass

	def clear_form(self) -> None:
		pass

	def save_and_back(self) -> None:
		''' Сделать запись в БД и вернуться на прошлую страницу '''

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

	def save(self, params: Dict[str, Widget]) -> None:
		''' Сделать запись в БД '''
		write_entry(self.model, params)

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		''' Валидация всех полей формы '''
		raise AttributeError('Сhild classes of _BaseCreateModel must have an is_valid method')

	def _pre_open_update(self) -> None:
		''' Обновление полей перед загрузкой окна '''
		pass


class TagCreateModel(_BaseCreateModel):
	''' Страница создания модели Tag '''

	name = 'create_tag'
	model = Tag
	toolbar_title = 'Создание Тега'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название', required=True,
			helper_text_mode='persistent', max_text_length=255, helper_text='',
			validators=[UniqueValidator(Tag, 'title'), EmptyValidator(Tag, 'title')])
		self.emergencies_field = FDMultiSelect(
			title='Вызовы',
			dialog_content=EmergencyDialogContent,
			model=Emergency)
		self.emergencies_field.bind_btn(
			lambda: self._path_manager.forward('create_emergency')
		)

		self.add_content(self.title_field)
		self.add_content(self.emergencies_field)

		self.params.update({
			'title': self.title_field,
			'emergencys': self.emergencies_field
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.emergencies_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.emergencies_field.set_value([])

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
				text='Поле "Название" должно быть уникальным',
				value=params['title'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class ShortCreateModel(_BaseCreateModel):
	''' Страница создания модели Short '''

	name = 'create_short'
	model = Short
	toolbar_title = 'Создание Сокращения'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название', required=True, helper_text_mode='persistent',
			max_text_length=255, helper_text='',
			validators=[UniqueValidator(Short, 'title'), EmptyValidator(None, None)])
		self.explanation_field = FDMultilineInput(
			hint_text='Полный текст',
			helper_text='Этот текст будет вставлен при нажатии в экране Вызова')
		self.into_new_line_field = FDDoubleSwitch(
			icon_active='text',
			icon_deactive='cursor-text',
			title_active='На новой строке',
			title_deactive='Продолжить строку')

		self.add_content(self.title_field)
		self.add_content(self.explanation_field)
		self.add_content(MDLabel(
			text='[b]Дополнительные элементы:[/b]\n' + \
			     'HH - [i]заполнится текущим часом;[/i]\n' + \
			     'MM - [i]заполнится текущей минутой;[/i]\n' + \
			     'SS - [i]заполнится текущей секундой;[/i]\n' + \
			     'yyyy - [i]заполнится текущим годом;[/i]\n' + \
			     'mm - [i]заполнится текущим месяцем;[/i]\n' + \
			     'dd - [i]заполнится текущим днем.[/i]',
			adaptive_height=True,
			markup=True,
			theme_text_color='Hint'
		))
		self.add_content(self.into_new_line_field)

		self.params.update({
			'title': self.title_field,
			'explanation': self.explanation_field,
			'into_new_line': self.into_new_line_field,
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.explanation_field.set_value('')

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
				text='Поле "Название" должно быть уникальным',
				value=params['title'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class RankCreateModel(_BaseCreateModel):
	''' Страница создания модели Rank '''

	name = 'create_rank'
	model = Rank
	toolbar_title = 'Создание Звания'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название', required=True, helper_text_mode='persistent',
			max_text_length=255, helper_text='',
			validators=[UniqueValidator(Rank, 'title'), EmptyValidator(None, None)])
		self.priority_field = FDNumberInput(
			hint_text='Приоритет',
			required=True,
			helper_text_mode='on_error',
			helper_text='',
			validators=[EmptyValidator(None, None)])
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda: self._path_manager.forward('create_human')
		)

		self.add_content(self.title_field)
		self.add_content(self.priority_field)
		self.add_content(self.humans_field)

		self.params.update({
			'title': self.title_field,
			'priority': self.priority_field,
			'humans': self.humans_field
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.humans_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.priority_field.set_value('')
		self.humans_field.set_value([])

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
				text='Поле "Название" должно быть уникальным',
				value=params['title']),
			EmptyValidator(self.model, 'priority')(
				text='Поле "Приоритет" не может быть пустым',
				value=params['priority'])
		)

		return tuple(filter(lambda check: not check.status, checks))


class PositionCreateModel(_BaseCreateModel):
	''' Страница создания модели Position '''

	name = 'create_position'
	model = Position
	toolbar_title = 'Создание Должности'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='',
			validators=[UniqueValidator(Position, 'title'), EmptyValidator(None, None)])
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda: self._path_manager.forward('create_human')
		)

		self.add_content(self.title_field)
		self.add_content(self.humans_field)

		self.params.update({
			'title': self.title_field,
			'humans': self.humans_field
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.humans_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.humans_field.set_value([])

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
				text='Поле "Название" должно быть уникальным',
				value=params['title']),
		)

		return tuple(filter(lambda check: not check.status, checks))


class HumanCreateModel(_BaseCreateModel):
	''' Страница создания модели Human '''

	name = 'create_human'
	model = Human
	toolbar_title = 'Создание Человека'

	def fill_elements(self) -> None:
		# title
		self.title_field = FDInput(
			hint_text='ФИО',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='',
			validators=[EmptyValidator(None, None), UniqueValidator(Human, 'title')])
		# phone_1
		self.phone_1_field = FDPhoneInput(
			hint_text='Телефон',
			max_text_length=255)
		# phone_2
		self.phone_2_field = FDPhoneInput(
			hint_text='Телефон (доп.)',
			max_text_length=255)
		# is_firefigher
		self.is_firefigher_field = FDDoubleSwitch(
			icon_active='fire-hydrant',
			icon_deactive=Human.icon,
			title_active='Пожарный',
			title_deactive='Комнатный')
		# work_date
		self.work_date_field = FDDate(
			icon='calendar',
			title='Рабочий день',
			btn_text='дд.мм.гггг')
		# start_vacation
		self.start_vacation_field = FDDate(
			icon='human-handsup',
			title='Начало отпуска',
			btn_text='дд.мм.гггг')
		# finish_vacation
		self.finish_vacation_field = FDDate(
			icon='briefcase',
			title='Конец отпуска',
			btn_text='дд.мм.гггг')
		# vacation dialog widget
		vacation_dates = (
			self.start_vacation_field.get_value(),
			self.finish_vacation_field.get_value())
		if None in vacation_dates:
			vacation_text = ''
		else:
			dts = map(lambda dt: dt.strftime('%d.%m.%Y'), vacation_dates)
			vacation_text = '{} - {}'.format(*dts)
		self.vacation_dialog_btn = FDButton(
			icon='human-handsup',
			title=f'Отпуск\n{vacation_text}',
			btn_text='Изменить')
		self.vacation_dialog_btn.ids.btn.bind(on_release=self.open_vacation_dialog)
		# worktype
		self.worktype_field = FDSelect(
			title='График работы',
			dialog_content=WorktypeDialogContent,
			model=Worktype,
			group='human_worktype')
		self.worktype_field.bind_btn(
			lambda: self._path_manager.forward('create_worktype')
		)
		# calendar
		self.calendar_field = FDCalendar()
		self.work_date_field.callback = lambda: self.calendar_field.select_work_days(
			work_day=self.work_date_field.get_value(),
			worktype=get_by_id(Worktype, self.worktype_field.get_value()),
			vacation=(self.start_vacation_field.get_value(),
			          self.finish_vacation_field.get_value()))
		self.worktype_field.bind_checkbox(lambda: self.calendar_field.select_work_days(
			work_day=self.work_date_field.get_value(),
			worktype=get_by_id(Worktype, self.worktype_field.get_value()),
			vacation=(self.start_vacation_field.get_value(),
			          self.finish_vacation_field.get_value())))
		# rank
		self.rank_field = FDSelect(
			title='Звание',
			dialog_content=RankDialogContent,
			model=Rank,
			group='human_rank')
		self.rank_field.bind_btn(
			lambda: self._path_manager.forward('create_rank')
		)
		# position
		self.position_field = FDSelect(
			title='Должность',
			dialog_content=PositionDialogContent,
			model=Position,
			group='human_position')
		self.position_field.bind_btn(
			lambda: self._path_manager.forward('create_position')
		)

		self.add_content(self.title_field)
		self.add_content(self.phone_1_field)
		self.add_content(self.phone_2_field)
		self.add_content(self.is_firefigher_field)
		self.add_content(self.work_date_field)
		# self.add_content(self.start_vacation_field)
		# self.add_content(self.finish_vacation_field)
		self.add_content(self.vacation_dialog_btn)
		self.add_content(self.calendar_field)
		self.add_content(self.worktype_field)
		self.add_content(self.rank_field)
		self.add_content(self.position_field)

		self.params.update({
			'title': self.title_field,
			'phone_1': self.phone_1_field,
			'phone_2': self.phone_2_field,
			'is_firefigher': self.is_firefigher_field,
			'work_day': self.work_date_field,
			'worktype': self.worktype_field,
			'rank': self.rank_field,
			'position': self.position_field,
			'start_vacation': self.start_vacation_field,
			'finish_vacation': self.finish_vacation_field
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.worktype_field.fill_elements()
		self.rank_field.fill_elements()
		self.position_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.phone_1_field.set_value('')
		self.phone_2_field.set_value('')
		self.is_firefigher_field.set_value(False)
		self.work_date_field.set_value(None)
		self.worktype_field.set_value([])
		self.rank_field.set_value([])
		self.position_field.set_value([])
		self.start_vacation_field.set_value(None)
		self.finish_vacation_field.set_value(None)

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "ФИО" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
				text='Поле "ФИО" должно быть уникальным',
				value=params['title']),
		)

		return tuple(filter(lambda check: not check.status, checks))

	def open_vacation_dialog(self, *args) -> None:
		''' Открыть диалог выбора дат отпуска '''

		content = MDBoxLayout(
			orientation='vertical',
			size_hint_y=None,
			height=dp(350))
		content.add_widget(self.start_vacation_field)
		content.add_widget(self.finish_vacation_field)
		content.add_widget(MDBoxLayout())

		ok_btn = MDRaisedButton(text='Ок')
		dialog = MDDialog(
			title='Отпуск',
			type='custom',
			content_cls=content,
			buttons=[ok_btn,]
		)
		ok_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()


class EmergencyCreateModel(_BaseCreateModel):
	''' Страница создания модели Emergency '''

	name = 'create_emergency'
	model = Emergency
	toolbar_title = 'Создание Вызова'

	def fill_elements(self) -> None:
		# title
		self.title_field = FDInput(
			hint_text='Название',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='',
			validators=[UniqueValidator(Emergency, 'title'), EmptyValidator(None, None)])
		# description
		self.description_field = FDMultilineInput(
			hint_text='Описание')
		# urgent
		self.urgent_field = FDSwitch(
			icon='truck-fast',
			title='Срочный?')
		# humans
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda: self._path_manager.forward('create_human')
		)
		# shorts
		self.shorts_field = FDMultiSelect(
			title='Сокращения',
			dialog_content=ShortDialogContent,
			model=Short)
		self.shorts_field.bind_btn(
			lambda: self._path_manager.forward('create_short')
		)
		# tags
		self.tags_field = FDMultiSelect(
			title='Теги',
			dialog_content=TagDialogContent,
			model=Tag)
		self.tags_field.bind_btn(
			lambda: self._path_manager.forward('create_tag')
		)

		self.add_content(self.title_field)
		self.add_content(self.description_field)
		self.add_content(self.urgent_field)
		self.add_content(self.humans_field)
		self.add_content(self.shorts_field)
		self.add_content(self.tags_field)

		self.params.update({
			'title': self.title_field,
			'description': self.description_field,
			'urgent': self.urgent_field,
			'tags': self.tags_field,
			'shorts': self.shorts_field,
			'humans': self.humans_field,
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.humans_field.fill_elements()
		self.shorts_field.fill_elements()
		self.tags_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.description_field.set_value('')
		self.urgent_field.set_value(False)
		self.tags_field.set_value([])
		self.shorts_field.set_value([])
		self.humans_field.set_value([])

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']
			),
			UniqueValidator(self.model, 'title')(
				text='Поле "Название" должно быть уникальным',
				value=params['title']
			),
		)

		return tuple(filter(lambda check: not check.status, checks))


class WorktypeCreateModel(_BaseCreateModel):
	''' Страница создания модели Worktype '''

	name = 'create_worktype'
	model = Worktype
	toolbar_title = 'Создание Графика работы'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='',
			validators=[UniqueValidator(Worktype, 'title'), EmptyValidator(None, None)])
		self.start_work_day_field = FDDateTime(
			title='Начало рабочего дня',
			btn1_text='чч:мм:сс',
			btn2_text='дд.мм.гггг')
		self.finish_work_day_field = FDDateTime(
			title='Конец рабочего дня',
			btn1_text='чч:мм:сс',
			btn2_text='дд.мм.гггг')
		self.work_day_range_field = FDNumberInput(
			hint_text='Рабочие дни подряд',
			required=True,
			helper_text_mode='on_error',
			helper_text='Поле не может быть пустым',
			validators=[ZeroValidator(self.model, 'work_day_range'),])
		self.week_day_range_field = FDNumberInput(
			hint_text='Выходные дни подряд',
			required=True,
			helper_text_mode='on_error',
			helper_text='Поле не может быть пустым')
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda *_: self._path_manager.forward('create_human')
		)

		self.add_content(self.title_field)
		self.add_content(self.start_work_day_field)
		self.add_content(self.finish_work_day_field)
		self.add_content(self.work_day_range_field)
		self.add_content(self.week_day_range_field)
		self.add_content(self.humans_field)

		self.params.update({
			'title': self.title_field,
			'start_work_day': self.start_work_day_field,
			'finish_work_day': self.finish_work_day_field,
			'work_day_range': self.work_day_range_field,
			'week_day_range': self.week_day_range_field,
			'humans': self.humans_field,
		})

	def _pre_open_update(self) -> None:
		if not self.was_opened:
			self.fill_elements()
			self.was_opened = True

		self.humans_field.fill_elements()

	def clear_form(self) -> None:
		self.title_field.set_value('')
		self.start_work_day_field.set_value(None)
		self.finish_work_day_field.set_value(None)
		self.work_day_range_field.set_value('')
		self.week_day_range_field.set_value('')
		self.humans_field.set_value([])

	def is_valid(self, params: Dict[str, Widget]) -> tuple:
		checks = (
			EmptyValidator(self.model, 'title')(
				text='Поле "Название" не может быть пустым',
				value=params['title']),
			UniqueValidator(self.model, 'title')(
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
