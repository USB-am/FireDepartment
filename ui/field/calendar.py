from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from config import CALENDAR_FIELD


Builder.load_file(CALENDAR_FIELD)


class FDCalendar(MDBoxLayout):
	''' Отображение календаря, отображающего график работы '''

	icon = 'calendar-multiselect-outline'
