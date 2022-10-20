import unittest
import datetime

from kivy.config import Config
Config.set('graphics', 'width', '1')
Config.set('graphics', 'height', '1')

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

	@classmethod
	def setUpClass(self):
		self.widget = fields.BooleanField(icon='test', title='Test')
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), False)

	def test_set_value(self):
		self.widget.set_value(True)
		self.assertEqual(self.widget.get_value(), True)


class TestDateField(unittest.TestCase):
	''' Тесты для виджета выбора даты '''

	@classmethod
	def setUpClass(self):
		self.widget = fields.DateField(icon='test', title='Test')
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), None)
		self.assertEqual(self.widget.ids.button.text, 'dd.mm.yyyy')

	def test_set_value(self):
		set_date = datetime.datetime.now().date()
		string_date = set_date.strftime('%d.%m.%Y')
		self.widget.set_value(set_date)
		self.assertEqual(self.widget.get_value(), set_date)
		self.assertEqual(self.widget.ids.button.text, string_date)


if __name__ == '__main__':
	unittest.main()