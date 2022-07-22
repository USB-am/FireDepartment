class PathManager:
	instance = None

	def __new__(cls, screen_manager=None):
		if PathManager.instance is None:
			return super().__new__(cls)
		else:
			return PathManager.instance

	def __init__(self, screen_manager=None):
		self.__screen_manager = screen_manager
		self.__path = ['main_page',]

	@property
	def current(self) -> str:
		return self.__path[-1]

	def _forward(self, screen_name: str) -> None:
		self.__path.append(screen_name)

	def _back(self) -> None:
		if len(self.__path) <= 1:
			return

		self.__path = self.__path[:-1]

	def back(self) -> None:
		self._back()
		self.__screen_manager.current = self.current

	def forward(self, screen_name: str) -> None:
		self._forward(screen_name)
		self.__screen_manager.current = self.current