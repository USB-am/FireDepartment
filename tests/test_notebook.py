import unittest
from datetime import datetime

from tests import AppTest
from data_base import *
from ui.widgets.notebook import FDNotebook


class TestNotebook(unittest.TestCase):
	''' Тестры виджета FDNotebook '''

	@classmethod
	def setUpClass(cls):
		cls.app = AppTest()
		cls.notebook = FDNotebook()
		cls.app.screen.add_widget(cls.notebook)

		cls.worktype_1_3 = Worktype(
			title='TestWorktype',
			start_work_day=datetime(2000, 1, 1, hour=9),
			finish_work_day=datetime(2000, 1, 2, hour=9),
			work_day_range=1,
			week_day_range=3
		)
		cls.worktype_5_2 = Worktype(
			title='TestWorktype',
			start_work_day=datetime(2000, 1, 1, hour=8),
			finish_work_day=datetime(2000, 1, 1, hour=17),
			work_day_range=5,
			week_day_range=2
		)
		cls.humans = [Human(
			title=f'Human #{i}',
			is_firefigher=bool(i%3),
			work_day=datetime(2000, 1, 2),
			worktype=cls.worktype_1_3 if i % 2 else cls.worktype_5_2
		) for i in range(100)]
		cls.emergency = Emergency(
			title='Emergency',
			description='',
			humans=cls.humans
		)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.notebook)

	def test_add_tab(self):
		''' Увеличение количества вкладок на панели сверху '''

		prev_top_tabs_count = len(self.notebook.ids.tab_panel.children)
		self.notebook.add_tab(self.emergency)
		now_top_tabs_count = len(self.notebook.ids.tab_panel.children)

		self.assertEqual(prev_top_tabs_count+1, now_top_tabs_count)
