# -*- coding: utf-8 -*-

import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from app.tools.path_manager import PathManager
from data_base import ColorTheme
from config import PATTERNS_DIR


def _get_bg_image() -> str:
	try:
		bg_image = ColorTheme.query.first().background_image

		if isinstance(bg_image, str) and not os.path.exists(bg_image):
			raise AttributeError()

	except AttributeError:
		bg_image = None

	return bg_image


path_to_kv_file = os.path.join(PATTERNS_DIR, 'custom_widgets', 'custom_screen.kv')
Builder.load_file(path_to_kv_file)


class CustomScreen(Screen):
	color = (0, 0, 0, 0) if _get_bg_image() is None else (1, 1, 1, 1)
	bg_image = _get_bg_image()

	def redirect_to_back_screen(self) -> None:
		to_screen_name = PathManager.back()
		self.manager.current = to_screen_name