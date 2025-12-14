from kivy.uix.screenmanager import Screen


class _BaseScreen(Screen):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
