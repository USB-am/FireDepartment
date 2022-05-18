# -*- coding: utf-8 -*-


def check_none_value(func):
	def wrapper(*args, **kwargs):
		if None in args and not kwargs:
			return

		return func(*args, **kwargs)

	return wrapper