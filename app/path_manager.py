from kivy.uix.screenmanager import ScreenManager, Screen


class PathManager:
	''' Менеджер путей '''

	def __init__(self, screen_manager: ScreenManager):
		self.__screen_manager = screen_manager
		self._path = ['main',]

	def forward(self, screen_name: str) -> Screen:
		self.__screen_manager.current = screen_name
		self._path.append(screen_name)

		return self.__screen_manager.current_screen

	def back(self) -> Screen:
		if len(self._path) > 1:
			self._path.pop(-1)

		self.__screen_manager.current = self._path[-1]

		return self.__screen_manager.current_screen