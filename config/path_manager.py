class PathManager:
	_instance = None
	_screen_manager = None
	_path = ['main_page',]

	def __new__(cls, screen_manager=None):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._screen_manager = screen_manager

		return cls._instance

	def current(self) -> str:
		return self._path[-1]

	def _forward(self, screen_name: str) -> None:
		self._path.append(screen_name)

	def _back(self) -> None:
		if len(self._path) <= 1:
			return

		self._path = self._path[:-1]

	def back(self) -> None:
		self._back()
		self._screen_manager.current = self.current()

	def forward(self, screen_name: str) -> None:
		self._forward(screen_name)
		self._screen_manager.current = self.current()