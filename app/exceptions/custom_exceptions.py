# -*- coding: utf-8 -*-


class DataBaseUpdateError(Exception):
	def __init__(self, entry_error):
		self._entry_error = entry_error

		super().__init__()

	def __str__(self) -> str:
		t = str(self._entry_error).split('\n')[0].split(' ')[-1]

		return f'Field {t} cannot be empty.'