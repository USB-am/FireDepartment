from kivy.properties import ListProperty, BooleanProperty


class _BaseWidget:
	validators = ListProperty([])
	error = BooleanProperty(False)

	def validate(self) -> bool:
		pass
