# -*- coding: utf-8 -*-

__all__ = ('PathManager', )


class _PathManager:
	PATH = ['main_page']

	def forward(self, page_name: str) -> None:
		self.PATH.append(page_name)

	def back(self) -> str:
		if len(self.PATH) > 1:
			self.PATH = self.PATH[:-1]

		return self.get_current_page_name

	@property
	def get_current_page_name(self) -> str:
		return self.PATH[-1]


PathManager = _PathManager()