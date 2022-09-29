import os

from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton

from config import UIX_KV_DIR, LOCALIZED
from data_base import db, Human, Rank, Position


path_to_kv_file = os.path.join(UIX_KV_DIR, 'dialog.kv')
Builder.load_file(path_to_kv_file)


class FDDialog(MDDialog):
	''' Всплывающее окно '''

	def __init__(self, title: str, content: MDBoxLayout,
	             buttons: list=[], **options):

		self.title = title
		self.content_cls = content
		self.type = 'custom'
		self.buttons = buttons

		super().__init__(**options)


class HumanDialogContent(MDBoxLayout):
	''' Всплывающее окно с информацией о человеке '''

	def __init__(self, human: Human):
		self.human = human
		self.name = human.title
		self.phone_1 = self._check_on_none(human.phone_1)
		self.phone_2 = self._check_on_none(human.phone_2)
		self.position = self._get_foreignkey(human.position, Position)
		self.rank = self._get_foreignkey(human.rank, Rank)

		super().__init__()

	def _check_on_none(self, attr) -> str:
		if attr is None:
			return LOCALIZED.translate('Pass')

		return str(attr)

	def _get_foreignkey(self, attr, table: db.Model) -> str:
		if attr is None:
			return LOCALIZED.translate('Pass')

		db_entry = table.query.get(attr)

		return db_entry.title


class ExceptionDialogContent(MDBoxLayout):
	''' Всплывающее окно с информацией об ошибке '''

	def __init__(self, text: str):
		self.exception_text = text

		super().__init__()