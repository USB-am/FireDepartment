class PathManager:
	instance = None

	def __new__(cls):
		if PathManager.instance is None:
			return super().__new__(cls)
		else:
			return PathManager.instance

	def __init__(self):
		self.__path = ['main_page',]

	@property
	def current(self) -> str:
		return self.__path[-1]

	def forward(self, screen_name: str) -> None:
		self.__path.append(screen_name)

	def back(self) -> None:
		if len(self.__path) <= 1:
			return

		self.__path = self.__path[:-1]