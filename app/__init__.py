from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from config import APP_SCREEN


class Application(MDApp):
	'''
	Базовый класс приложения. Инициализирует интерфейс и добавляет страницы.
	'''

	color = [1, 1, 1, 1]
	bg_image = None

	def build(self):
		return Builder.load_file(APP_SCREEN)