from kivy.uix.screenmanager import ScreenManager, Screen


class PathManager:
	''' Менеджер путей '''

	_instance = None

	def __new__(cls, *args):
		if cls._instance is None:
			cls._instance = super(PathManager, cls).__new__(cls)

		return cls._instance

	def __init__(self, screen_manager: ScreenManager):
		if screen_manager is None:
			self.__screen_manager = self._instance.__screen_manager
		else:
			self.__screen_manager = screen_manager
		self._path = ['main',]
		print(f'self._instance = {self._instance}\n{self}')

	def forward(self, screen_name: str) -> Screen:
		self.__screen_manager.current = screen_name
		self._path.append(screen_name)

		return self.__screen_manager.current_screen

	def back(self) -> Screen:
		if len(self._path) > 1:
			self._path.pop(-1)

		self.__screen_manager.current = self._path[-1]

		return self.__screen_manager.current_screen