from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from data_base import db
from config import SELECT_LAYOUTS


Builder.load_file(SELECT_LAYOUTS)


class FDSelectListElement(MDBoxLayout):
	'''
	Элемент списка виджета FDSelect и FDMultiSelect.

	~params:
	entry: db.Model - запись из БД;
	info_content: MDBoxLayout - область с информацией о записи;
	group: str - название группы элементов. Если значение None, поведение как Checkbox.
	'''

	def __init__(self, entry: db.Model, info_content: MDBoxLayout, group: str=None):
		self.entry = entry
		self.info_content = info_content
		self.group = group

		super().__init__()

		self.ids.info_btn.bind(on_release=lambda *_: self.open_info_dialog())

	def open_info_dialog(self) -> None:
		''' Открыть диалоговое окно с информацией '''
		
		ok_btn = MDRaisedButton(text='Ок')
		dialog = MDDialog(
			title='Информация',
			type='custom',
			content_cls=self.info_content(self.entry),
			buttons=[ok_btn]
		)
		ok_btn.bind(on_release=lambda *_: dialog.dismiss())

		dialog.open()
