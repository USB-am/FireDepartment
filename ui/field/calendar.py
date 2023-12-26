from datetime import datetime, date

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from data_base import Worktype
from config import CALENDAR_FIELD


Builder.load_file(CALENDAR_FIELD)


class FDCalendar(MDBoxLayout):
	'''
	Отображение календаря, отображающего график работы.

	~params:
	start_work_day: date - день для начала отсчета;
	worktype: Worktype - запись из БД о графике работы.
	'''

	icon = 'calendar-month'

	def __init__(self, start_work_day: date, worktype: Worktype, **options):
		self.start_work_day = start_work_day
		self.worktype = worktype

		super().__init__(**options)

		layout = self.ids.calendar_layout
		for i in range(-5, 31):
			layout.add_widget(MDLabel(
				text=str(i+1),
				md_bg_color=(1, 0, 0, .3),
				radius=10,
				size_hint=(None, None),
				size=(20, 20),
				halign='center',
				valign='center'
			))

	def update(self,
	           start_work_day: date=None,
	           worktype: Worktype=None
	          ) -> None:
		'''
		Производит перерасчет рабочего времени.

		~params:
		start_work_day: date=None - день для начала отсчета;
		worktype: Worktype=None - запись из БД о графике работы.
		'''

		if start_work_day is not None:
			self.start_work_day = start_work_day
		if worktype is not None:
			self.worktype = worktype

		print(f'FDCalendar.update() is started')
