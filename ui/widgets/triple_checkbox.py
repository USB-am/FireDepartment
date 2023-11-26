from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BoundedNumericProperty
from kivymd.uix.boxlayout import MDBoxLayout

from config import TRIPLE_CHECKBOX


Builder.load_file(TRIPLE_CHECKBOX)


class FDTripleCheckbox(MDBoxLayout):
	''' Область с тройным чекбоксом. '''

	normal_icon = StringProperty()
	active_icon = StringProperty()
	deactive_icon = StringProperty()
	title = StringProperty()
	substring = StringProperty('')
	state = BoundedNumericProperty(0, min=0, max=2)

	def click(self) -> None:
		''' Обработка изменения состояния при клике '''

		self.state = (self.state + 1) % 3

		if self.state == 0:
			self.md_bg_color = [0, 0, 0, 0]
			self.ids.checkbox.icon = self.normal_icon
		elif self.state == 1:
			self.md_bg_color = [0, 1, 0, .3]
			self.ids.checkbox.icon = self.active_icon
		elif self.state == 2:
			self.md_bg_color = [1, 0, 0, .3]
			self.ids.checkbox.icon = self.deactive_icon

	def get_value(self) -> int:
		''' Возвращает текущее состояние виджета '''

		return self.state

	def set_value(self, state: int) -> None:
		''' Устанавливает состояние виджету '''
		if state is not None:
			self.state = state % 3