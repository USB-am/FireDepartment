from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __FIELD_BUTTON


Builder.load_file(__FIELD_BUTTON)


class FDCenterButton(AnchorLayout):
	''' Небольшая кнопка по середине '''

	text = StringProperty()


class FDSubmit(AnchorLayout):
	''' Закрашенная кнопка по середине '''

	text = StringProperty()


class FDIconLabelButton(MDBoxLayout):
	''' Иконка | Текст | Кнопка '''

	icon = StringProperty()
	text = StringProperty()
	button_text = StringProperty()