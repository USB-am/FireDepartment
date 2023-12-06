from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout

from config import DIALOG_LAYOUTS
from data_base import db, Tag
from ui.field.label import FDTitle, FDVerticalLabel
from ui.field.button import FDIconButton


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

		self.ids.content.add_widget(FDVerticalLabel(
			title='Название',
			value=entry.title
		))

		if entry.emergencys:
			self.ids.content.add_widget(FDTitle(
				title='Связан с Вызовами:'
			))

			sorted_emergencies = sorted(entry.emergencys, key=lambda e: e.title)
			for emergency in sorted_emergencies:
				btn = FDIconButton(
					icon=emergency.icon,
					icon_btn='eye',
					title=emergency.title
				)
				btn.bind_btn(lambda e=emergency: print(f'View {e.title} emergency'))

				self.ids.content.add_widget(btn)
