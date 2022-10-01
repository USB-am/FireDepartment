from kivymd.uix.button import MDIconButton


class TripleCheckbox(MDIconButton):
	''' Чекбокс с 3 состояниями '''

	def __init__(self, state_normal: str, state_ok: str, state_cancel: str):
		super().__init__()

		self.states = [
			state_normal,	# phone-settings-outline
			state_ok,	# phone-in-talk
			state_cancel	# phone-cancel
		]
		self._increment = 0
		self.icon = self.states[self.increment]

		self.bind(on_release=lambda e: self.click())

	@property
	def increment(self) -> int:
		return self._increment

	@increment.setter
	def increment(self, *_) -> None:
		self._increment = (self.increment + 1) % 3

	def click(self) -> None:
		self.increment += 1

		self.icon = self.states[self.increment]