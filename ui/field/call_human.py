from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout

from ui.widgets.triple_checkbox import FDTripleCheckbox	# used in the .kv file
from config import CALL_HUMAN_FIELD_KV


Builder.load_file(CALL_HUMAN_FIELD_KV)


class FDCallHumanField(MDBoxLayout):
	''' Поле с вызываемым человеком '''

	def __init__(self, human: 'Human'):
		self.human = human

		super().__init__()

		self.checkbox = self.ids.triple_checkbox
		self.checkbox.icon = 'phone'
		self.checkbox.icons = ('phone', 'phone-check', 'phone-remove')
		self.checkbox.bind(on_release=lambda _: self._update_color())

	def _update_color(self) -> None:
		''' Обновить цвет фона в зависимости от состояния чекбокса '''

		colors = [(0, 0, 0, 0), (0, 1, 0, .2), (1, 0, 0, .2)]
		self.md_bg_color = colors[(self.checkbox.state_+1)%3]
