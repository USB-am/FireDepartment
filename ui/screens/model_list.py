from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Rank, Position, Human, Emergency, Worktype
from ui.layout.model_list_element import ModelListElement
from ui.layout.dialogs import TagDialogContent, RankDialogContent, \
	PositionDialogContent, HumanDialogContent, EmergencyDialogContent,\
	WorktypeDialogContent


class _ModelList(BaseScrollScreen):
	''' Базовый класс с элементами из базы данных '''

	def __init__(self, path_manager: PathManager):
		super().__init__(path_manager)
		self.dialog = None

		self.ids.toolbar.add_left_button(
			icon='menu',
			callback=self.open_menu
		)
		self.ids.toolbar.add_right_button(
			icon='file-plus',
			callback=lambda *_: self._path_manager.forward(
				f'create_{self.model.__tablename__.lower()}'
		))

		self.bind(on_pre_enter=lambda *_: self.fill_elements())

	def fill_elements(self) -> None:
		self.clear_content()

	def open_info_dialog(self, content: MDBoxLayout) -> None:
		''' Открыть диалогов окно с информацией '''

		ok_btn = MDRaisedButton(text='Ок')
		dialog = MDDialog(
			title='Информация',
			type='custom',
			content_cls=content,
			buttons=[ok_btn]
		)
		ok_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()

	def move_to_edit_and_fill_fields(self, entry: db.Model) -> None:
		'''
		Перейти на экран редактирования записи.

		~params:
		entry: db.Model - запись, которая будет редактироваться.
		'''

		next_screen = self._path_manager.forward(
			f'edit_{self.model.__tablename__.lower()}')
		next_screen.fill_fields(entry)


class TagsList(_ModelList):
	''' Класс с элементами из модели Tag '''

	name = 'tags_list'
	model = Tag
	toolbar_title = 'Теги'
	info_dialog_content = TagDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		tags = self.model.query.order_by(Tag.title).all()

		for tag in tags:
			list_elem = ModelListElement(entry=tag, icon=Tag.icon)
			list_elem.bind_edit_btn(
				lambda t=tag: self.move_to_edit_and_fill_fields(t))
			list_elem.bind_info_btn(
				lambda t=tag: self.open_info_dialog(self.info_dialog_content(t))
			)
			self.add_content(list_elem)


class RanksList(_ModelList):
	''' Класс с элементами из модели Rank '''

	name = 'ranks_list'
	model = Rank
	toolbar_title = 'Звания'
	info_dialog_content = RankDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		ranks = self.model.query.order_by(Rank.title).all()

		for rank in ranks:
			list_elem = ModelListElement(entry=rank, icon=Rank.icon)
			list_elem.bind_edit_btn(
				lambda r=rank: self.move_to_edit_and_fill_fields(r))
			list_elem.bind_info_btn(
				lambda r=rank: self.open_info_dialog(self.info_dialog_content(r))
			)
			self.add_content(list_elem)


class PositionsList(_ModelList):
	''' Класс с элементами из модели Position '''

	name = 'positions_list'
	model = Position
	toolbar_title = 'Должности'
	info_dialog_content = PositionDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		positions = self.model.query.order_by(Position.title).all()

		for position in positions:
			list_elem = ModelListElement(entry=position, icon=Position.icon)
			list_elem.bind_edit_btn(
				lambda p=position: self.move_to_edit_and_fill_fields(p))
			list_elem.bind_info_btn(
				lambda p=position: self.open_info_dialog(self.info_dialog_content(p))
			)
			self.add_content(list_elem)


class HumansList(_ModelList):
	''' Класс с элементами из модели Human '''

	name = 'humans_list'
	model = Human
	toolbar_title = 'Сотрудники'
	info_dialog_content = HumanDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		humans = self.model.query.order_by(Human.title).all()

		for human in humans:
			i = 'fire-hydrant' if human.is_firefigher else Human.icon
			list_elem = ModelListElement(
				entry=human,
				icon=i
			)
			list_elem.bind_edit_btn(
				lambda h=human: self.move_to_edit_and_fill_fields(h))
			list_elem.bind_info_btn(
				lambda h=human: self.open_info_dialog(self.info_dialog_content(h))
			)
			self.add_content(list_elem)


class EmergenciesList(_ModelList):
	''' Класс с элементами из модели Emergency '''

	name = 'emergencies_list'
	model = Emergency
	toolbar_title = 'Вызовы'
	info_dialog_content = EmergencyDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		emergencies = self.model.query.order_by(Emergency.title).all()

		for emergency in emergencies:
			list_elem = ModelListElement(entry=emergency, icon=Emergency.icon)
			list_elem.bind_edit_btn(
				lambda e=emergency: self.move_to_edit_and_fill_fields(e))
			list_elem.bind_info_btn(
				lambda e=emergency: self.open_info_dialog(self.info_dialog_content(e))
			)
			self.add_content(list_elem)


class WorktypesList(_ModelList):
	''' Класс с элементами из модели Worktype '''

	name = 'worktypes_list'
	model = Worktype
	toolbar_title = 'Графики работы'
	info_dialog_content = WorktypeDialogContent

	def fill_elements(self) -> None:
		self.clear_content()
		worktypes = self.model.query.order_by(Worktype.title).all()

		for worktype in worktypes:
			list_elem = ModelListElement(entry=worktype, icon=Worktype.icon)
			list_elem.bind_edit_btn(
				lambda wt=worktype: self.move_to_edit_and_fill_fields(wt))
			list_elem.bind_info_btn(
				lambda wt=worktype: self.open_info_dialog(self.info_dialog_content(wt))
			)
			self.add_content(list_elem)
