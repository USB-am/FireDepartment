from kivymd.uix.button import MDIconButton


class FDTripleCheckbox(MDIconButton):
	''' Чекбокс с 3 состояниями нажатия '''

	def __init__(self, normal: str='', active: str='', deactive: str='', **options):
		self.icons = [normal, active, deactive]
		self.state_ = 0

		super().__init__(icon=normal, **options)

		self.bind(on_release=lambda _: self.click())

	def click(self) -> None:
		self.state_ = (self.state_ + 1) % 3
		self.icon = self.icons[self.state_]
