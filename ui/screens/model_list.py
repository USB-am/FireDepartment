from typing import Type

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from . import BaseScrollScreen
from app.path_manager import PathManager
from data_base import db, Tag, Rank, Position, Human, Emergency
from ui.layout.model_list_element import ModelListElement
from ui.layout.dialogs import TagDialogContent


__all__ = ('TagsList',)


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
			callback=None
		)

		self.fill_elements()

	def fill_elements(self) -> None:
		pass

	def open_info_dialog(self, content: MDBoxLayout) -> None:
		''' Открыть диалогов окно с информацией '''

		if self.dialog is None:
			ok_btn = MDRaisedButton(text='Ок')
			ok_btn.bind(on_release=lambda *_: self.close_info_dialog())
			self.dialog = MDDialog(
				title='Информация',
				type='custom',
				content_cls=content,
				buttons=[ok_btn]
			)

		self.dialog.open()

	def close_info_dialog(self) -> None:
		''' Закрыть диалоговое окно с информацией '''

		if self.dialog is None:
			return

		self.dialog.dismiss()


class TagsList(_ModelList):
	''' Класс с элементами из модели Tag '''

	name = 'tags_list'
	model = Tag
	toolbar_title = 'Теги'
	info_dialog_content = TagDialogContent

	def fill_elements(self) -> None:
		tags = self.model.query.order_by(Tag.title).all()

		for tag in tags:
			list_elem = ModelListElement(entry=tag, icon=Tag.icon)
			list_elem.bind_edit_btn(lambda t=tag: print(f'Edit btn {t.title}'))
			list_elem.bind_info_btn(
				lambda t=tag: self.open_info_dialog(self.info_dialog_content(t))
			)
			self.add_content(list_elem)


class RanksList(_ModelList):
	''' Класс с элементами из модели Rank '''

	name = 'ranks_list'
	model = Rank
	toolbar_title = 'Звания'

	def fill_elements(self) -> None:
		ranks = self.model.query.order_by(Rank.title).all()

		for rank in ranks:
			list_elem = ModelListElement(entry=rank, icon=Rank.icon)
			list_elem.bind_edit_btn(lambda r=rank: print(f'Edit btn {r.title}'))
			list_elem.bind_info_btn(lambda r=rank: print(f'Info btn {r.title}'))
			self.add_content(list_elem)


class PositionsList(_ModelList):
	''' Класс с элементами из модели Position '''

	name = 'positions_list'
	model = Position
	toolbar_title = 'Должности'

	def fill_elements(self) -> None:
		positions = self.model.query.order_by(Position.title).all()

		for position in positions:
			list_elem = ModelListElement(entry=position, icon=Position.icon)
			list_elem.bind_edit_btn(lambda p=position: print(f'Edit btn {p.title}'))
			list_elem.bind_info_btn(lambda p=position: print(f'Info btn {p.title}'))
			self.add_content(list_elem)


class HumansList(_ModelList):
	''' Класс с элементами из модели Human '''

	name = 'humans_list'
	model = Human
	toolbar_title = 'Сотрудники'

	def fill_elements(self) -> None:
		humans = self.model.query.order_by(Human.title).all()

		for human in humans:
			i = 'fire-hydrant' if human.is_firefigher else Human.icon
			list_elem = ModelListElement(
				entry=human,
				icon=i
			)
			list_elem.bind_edit_btn(lambda h=human: print(f'Edit btn {h.title}'))
			list_elem.bind_info_btn(lambda h=human: print(f'Info btn {h.title}'))
			self.add_content(list_elem)


class EmergenciesList(_ModelList):
	''' Класс с элементами из модели Emergency '''

	name = 'emergencies_list'
	model = Emergency
	toolbar_title = 'Вызовы'

	def fill_elements(self) -> None:
		emergencies = self.model.query.order_by(Emergency.title).all()

		for emergency in emergencies:
			list_elem = ModelListElement(entry=emergency, icon=Emergency.icon)
			list_elem.bind_edit_btn(lambda e=emergency: print(f'Edit btn {e.title}'))
			list_elem.bind_info_btn(lambda e=emergency: print(f'Info btn {e.title}'))
			self.add_content(list_elem)
