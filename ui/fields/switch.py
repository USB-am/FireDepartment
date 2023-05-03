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
		if value is None:
			value = False

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
		if value is None:
			value = False

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


class FDTripleCheckbox(MDBoxLayout):
	''' Checkbox с тремя состояниями '''

	normal_icon = StringProperty('phone-settings')
	active_icon = StringProperty('phone-check')
	deactive_icon = StringProperty('phone-cancel')
	title = StringProperty()
	substring = StringProperty('')
	_state = 0

	def click(self) -> None:
		self._state = (self._state + 1) % 3

		if self._state == 0:
			self.md_bg_color = [0, 0, 0, 0]
			self.ids.icon_btn.icon = self.normal_icon
		elif self._state == 1:
			self.md_bg_color = [0, 1, 0, .3]
			self.ids.icon_btn.icon = self.active_icon
		elif self._state == 2:
			self.md_bg_color = [1, 0, 0, .3]
			self.ids.icon_btn.icon = self.deactive_icon

	def get_value(self) -> int:
		return self._state

	def set_value(self, value: int) -> None:
		if value is None:
			return

		self._state = value % 3