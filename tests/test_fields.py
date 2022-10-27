import unittest
import datetime

from kivy.config import Config
Config.set('graphics', 'width', '1')
Config.set('graphics', 'height', '1')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from uix import fields
from data_base import Emergency


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


class TestDateTimeField(unittest.TestCase):
	''' Тесты для видже выбора даты и времени '''

	@classmethod
	def setUpClass(self):
		self.widget = fields.DateTimeField(icon='test', title='Test', help_text='Test')
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), None)

	def test_set_value(self):
		date = datetime.datetime.strptime(
			'01.01.1970 01:00:00', '%d.%m.%Y %H:%M:%S')
		self.widget.set_value(date)

		self.assertEqual(self.widget.get_value(), date)

	def test_set_date(self):
		date = datetime.datetime.now().date()
		button_date = date.strftime('%d.%m.%Y')
		self.widget.set_date(date)

		self.assertEqual(self.widget.ids.date_button.text, button_date)

	def test_set_time(self):
		time = datetime.datetime.now().time()
		button_time = time.strftime('%H:%M:%S')
		self.widget.set_time(time)

		self.assertEqual(self.widget.ids.time_button.text, button_time)


class TestSelectedList(unittest.TestCase):
	''' Тесты для SelectedList '''

	@classmethod
	def setUpClass(self):
		self.widget = fields.SelectedList(
			icon='test',
			title='Test',
			values=Emergency.query.all()
		)
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), [])

	def test_set_value(self):
		values = Emergency.query.all()
		self.widget.set_value([values[0], values[2]])

		self.assertEqual(self.widget.get_value(), [values[2], values[0]])


class TestSelectedListGroup(unittest.TestCase):
	''' Тесты для SelectedList с аргументом group '''

	@classmethod
	def setUpClass(self):
		self.widget = fields.SelectedList(
			icon='test',
			title='Test',
			values=Emergency.query.all(),
			group='test_group'
		)
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()

	def test_get_value(self):
		self.assertEqual(self.widget.get_value(), [])

	def test_set_value(self):
		values = Emergency.query.all()
		self.widget.set_value([values[0], values[2]])

		self.assertEqual(self.widget.get_value(), [values[0],])


if __name__ == '__main__':
	unittest.main()