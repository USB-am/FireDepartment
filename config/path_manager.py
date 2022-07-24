class PathManager:
	instance = None
	_screen_manager = None
	_path = ['main_page',]

	def __new__(cls, screen_manager=None):
		if PathManager.instance is None:
			PathManager.instance = super().__new__(cls)
			PathManager._screen_manager = screen_manager

		return PathManager.instance

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
		print(f'Current = {self.current()} [{type(self.current())}]')
		self._screen_manager.current = self.current()