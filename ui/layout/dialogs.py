from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from config import DIALOG_LAYOUTS
from data_base import db, Tag


Builder.load_file(DIALOG_LAYOUTS)


class _BaseDialogContent(MDBoxLayout):
	'''
	Базовый класс содержимого всплывающего окна.

	~params:
	entry: db.Model - запись из модели.
	'''

	entry = ObjectProperty(defaultvalue=db.Model)

	def add_content(self, widget: Widget) -> None:
		'''
		Добавляет виджет на фрейм контента.

		~params:
		widget: Widget - виджет, который будет отображен.
		'''

		self.ids.content.add_widget(widget)


class TagDialogContent(_BaseDialogContent):
	'''
	Содержимое всплывающего окна с информацией о записи из модели Tag.

	~params:
	entry: Tag - запись из модели Tag.
	'''

	def __init__(self, entry: Tag, **options):
		super().__init__(entry=entry, **options)
