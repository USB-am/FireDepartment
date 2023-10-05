from kivy.lang.builder import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config.paths import __FIELD_SWITCH


Builder.load_file(__FIELD_SWITCH)


class FDSwitch(MDBoxLayout):
	''' Виджет с переключателем '''

	icon = StringProperty()
	title = StringProperty()


class FDStateSwitch(MDBoxLayout):
	''' Виджет с переключающейся иконкой '''

	active_icon = StringProperty()
	deactive_icon = StringProperty()
	title = StringProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.ids.switch.bind(on_release=self._update_icon)

	def _update_icon(self, *_) -> None:
		icon_widget = self.ids.icon

		if icon_widget.icon == self.active_icon:
			icon_widget.icon = self.deactive_icon
		elif icon_widget.icon == self.deactive_icon:
			icon_widget.icon = self.active_icon

	def get_value(self) -> bool:
		return self.ids.switch.active

	def set_value(self, value: bool) -> None:
		self.ids.switch.active = value
		self._update_icon()
