import datetime
import unittest

from kivy.config import Config
Config.set('graphics', 'width', '1')
Config.set('graphics', 'height', '1')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen

from uix import notebook
from data_base import db, Human, Worktype


class ApplicationForTests(MDApp):
	''' Родительское окно для тестирования '''

	def __init__(self):
		super().__init__()

		self.screen_manager = ScreenManager()
		self.screen_manager.add_widget(Screen())

	def get_screen(self):
		return self.screen_manager.current_screen


APP = ApplicationForTests()


class TestNotebook(unittest.TestCase):
	''' Тесты для FDNoteBook '''

	@classmethod
	def setUpClass(self):
		self.widget = notebook.FDNoteBook()
		APP.get_screen().add_widget(self.widget)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()


class TestWeekFilter(unittest.TestCase):
	''' Тексты для фильтра работающих людей '''

	@classmethod
	def setUpClass(self):
		wt = Worktype(
			title='1/3',
			start_work_day=datetime.datetime(2022, 10, 3, 9),
			finish_work_day=datetime.datetime(2022, 10, 4, 9),
			work_day_range=1,
			week_day_range=3
		)
		h = Human(
			title='TestHuman',
			work_day=datetime.date(2022, 10, 3),
			worktype=2
		)
		self.humans = [h,]

		# self.humans = Human.query.all()
		self._filter = notebook.Filter(self.humans)

	@classmethod
	def tearDownClass(self):
		APP.get_screen().clear_widgets()
		db.session.rollback()

	def test_is_works(self):
		dt = datetime.date(2022, 10, 11)
		output = self._filter._is_works(dt, self.humans[0])

		self.assertEqual(output, True)