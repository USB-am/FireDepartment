from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import COLORS_FIELD


Builder.load_file(COLORS_FIELD)


class FDColor(MDBoxLayout):
	''' Поле выбора цвета из палитры '''

	icon = StringProperty()
	title = StringProperty()