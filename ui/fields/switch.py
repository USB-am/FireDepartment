from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import paths


Builder.load_file(paths.SWITCH_FIELD)


class FDSwitch(MDBoxLayout):
	''' Переключатель '''

	icon = StringProperty()
	title = StringProperty()

	def get_value(self) -> bool:
		return self.ids.switch.active

	def set_value(self, value: bool) -> None:
		self.ids.switch.active = value


class FDStatusSwitch(MDBoxLayout):
	''' Переключатель с меняющейся иконкой '''

	active_icon = StringProperty()
	active_title = StringProperty()
	deactive_icon = StringProperty()
	deactive_title = StringProperty()

	def get_value(self) -> bool:
		return self.ids.switch.active

	def set_value(self, value: bool) -> None:
		self.ids.switch.active = value
		self.update()

	def update(self) -> None:
		status = self.ids.switch.active

		if status:
			self.ids.icon.icon = self.active_icon
			self.ids.title.text = self.active_title
		else:
			self.ids.icon.icon = self.deactive_icon
			self.ids.title.text = self.deactive_title