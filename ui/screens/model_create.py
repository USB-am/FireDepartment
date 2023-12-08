from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Rank, Position, Human, Emergency
from ui.field.input import FDInput, FDNumberInput, FDPhoneInput
from ui.field.button import FDRectangleButton
from ui.field.select import FDMultiSelect
from ui.field.switch import FDDoubleSwitch
from ui.layout.dialogs import HumanDialogContent, EmergencyDialogContent


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
			callback=lambda *_: print('Save button is pressed!')
		)

		self.fill_elements()

	def fill_elements(self) -> None:
		pass


class TagCreateModel(_BaseCreateModel):
	''' Страница создания модели Tag '''

	name = 'create_tag'
	model = Tag
	toolbar_title = 'Создание Тега'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название', required=True,
			helper_text_mode='on_error', max_text_length=255,
			helper_text='Поле не может быть пустым или неуникальным')
		self.emergencies_field = FDMultiSelect(
			title='Вызовы',
			dialog_content=EmergencyDialogContent,
			model=Emergency)
		self.emergencies_field.bind_btn(
			lambda: self._path_manager.forward('create_emergency')
		)
		self.save_btn = FDRectangleButton(title='Сохранить')

		self.add_content(self.title_field)
		self.add_content(self.emergencies_field)
		self.add_content(self.save_btn)


class RankCreateModel(_BaseCreateModel):
	''' Страница создания модели Rank '''

	name = 'create_rank'
	model = Rank
	toolbar_title = 'Создание Звания'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='Название',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='Поле не может быть пустым или неуникальным')
		self.priority_field = FDNumberInput(
			hint_text='Приоритет',
			required=True,
			helper_text_mode='on_error',
			helper_text='Поле не может быть пустым')
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda: self._path_manager.forward('create_human')
		)
		self.save_btn = FDRectangleButton(title='Сохранить')

		self.add_content(self.title_field)
		self.add_content(self.priority_field)
		self.add_content(self.humans_field)
		self.add_content(self.save_btn)


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
			helper_text='Поле не может быть пустым или неуникальным')
		self.humans_field = FDMultiSelect(
			title='Люди',
			dialog_content=HumanDialogContent,
			model=Human)
		self.humans_field.bind_btn(
			lambda: self._path_manager.forward('create_human')
		)
		self.save_btn = FDRectangleButton(title='Сохранить')

		self.add_content(self.title_field)
		self.add_content(self.humans_field)
		self.add_content(self.save_btn)


class HumanCreateModel(_BaseCreateModel):
	''' Страница создания модели Human '''

	name = 'create_human'
	model = Human
	toolbar_title = 'Создание Человека'

	def fill_elements(self) -> None:
		self.title_field = FDInput(
			hint_text='ФИО',
			required=True,
			helper_text_mode='on_error',
			max_text_length=255,
			helper_text='Поле не может быть пустым')
		self.phone_1_field = FDPhoneInput(
			hint_text='Телефон',
			max_text_length=255)
		self.phone_2_field = FDPhoneInput(
			hint_text='Телефон (доп.)',
			max_text_length=255)
		self.is_firefigher_field = FDDoubleSwitch(
			icon_active='fire-hydrant',
			icon_deactive=Human.icon,
			title_active='Пожарный',
			title_deactive='Комнатный')

		self.save_btn = FDRectangleButton(title='Сохранить')

		self.add_content(self.title_field)
		self.add_content(self.phone_1_field)
		self.add_content(self.phone_2_field)
		self.add_content(self.is_firefigher_field)
		self.add_content(self.save_btn)
