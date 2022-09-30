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
		self._state = 0

		self.bind(on_release=lambda e: self.click())

	@property
	def state(self) -> int:
		return self._state

	@state.setter
	def state(self, value: int) -> None:
		self._state = (self.state + value) % 3

	def click(self) -> None:
		self.state += 1

		self.icon = self.states[self.state]
		# TODO: Update color