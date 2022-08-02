from os import path

from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout

from config import FIELDS_DIR, LOCALIZED


path_to_kv_file = path.join(FIELDS_DIR, 'label.kv')
Builder.load_file(path_to_kv_file)


class FDLabel(MDBoxLayout):
	'''
	Виджет класса отображения текста. Имеет вид: 
	title: content
	'''
	def __init__(self, title: str, content: str):
		self.title = title
		self.content = content
		self.display_title = LOCALIZED.translate(title)
		self.display_content = LOCALIZED.translate(content)

		super().__init__()


class FDIcon(MDBoxLayout):
	'''
	Виджет класса отображения иконки с текстом. Имеет вид:
	[иконка] текст
	'''
	def __init__(self, icon: str, content: str, **options):
		self.icon = icon
		self.content = content
		self.display_content = LOCALIZED.translate(content)

		super().__init__(**options)


class FDTitleLabel(MDTextField):
	'''
	Виджет класса отображения текста с заголовком. Имеет вид:
	TITLE: text
	'''
	icon = 'cursor-text'

	def __init__(self, title: str, text: str):
		self.title = title

		super().__init__()

		self.text = text if text is not None else ''


class FDEntry(MDTextField):
	''' Поле ввода текста '''
	def __init__(self, title: str):
		self.title = title
		self.display_title = LOCALIZED.translate(title)

		super().__init__()

	def get_value(self) -> str:
		return self.text

	def set_value(self, value: str) -> None:
		if value is None:
			value = ''

		self.text = value


class FDTextArea(FDEntry):
	''' Многострочное поле ввода текста '''
	pass