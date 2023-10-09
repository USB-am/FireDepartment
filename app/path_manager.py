from kivy.uix.screenmanager import ScreenManager, Screen


class _Singleton(type):
	_instance = None

	def __call__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(_Singleton, cls).__call__(*args, **kwargs)

		return cls._instance


class PathManager(metaclass=_Singleton):
	''' Менеджер путей '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager
		self._path = ['main',]

	def forward(self, screen_name: str) -> Screen:
		self.__screen_manager.current = screen_name
		self._path.append(screen_name)
		print(self._path)

		return self.__screen_manager.current_screen

	def back(self) -> Screen:
		if len(self._path) > 1:
			self._path.pop(-1)

		self.__screen_manager.current = self._path[-1]
		print(self._path)

		return self.__screen_manager.current_screen

	def move_to_screen(self, screen_name: str) -> Screen:
		self._path = ['main',]
		self.forward(screen_name)