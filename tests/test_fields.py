import unittest

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from uix import fields
from custom_screen import CustomScreen


class ApplicationForTests(MDApp):
	''' Родительское окно для тестирования '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(Screen())

	def get_screen(self):
		return self.screen_manager.current_screen


APP = ApplicationForTests()


class TestBooleanField(unittest.TestCase):
	''' Тесты для BooleanField '''

	def setUpClass(self):
		self.widget = fields.BooleanField(icon='test', title='Test')
		APP.get_screen().add_widget(self.widget)

	def tearDownClass(self):
		APP.get_screen().clear_widgets()
		print('Clear all widgets')

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), False)

	def test_set_value(self):
		self.widget.set_value(True)
		self.assertEqual(self.widget.get_value(), True)


if __name__ == '__main__':
	unittest.main()