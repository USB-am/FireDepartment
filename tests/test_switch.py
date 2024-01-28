import unittest

from tests import AppTest
from ui.field.switch import FDSwitch, FDDoubleSwitch


class TestFDSwitch(unittest.TestCase):
	''' Тесты FDSwitch '''

	@classmethod
	def setUpClass(cls):
		cls.app = AppTest()
		cls.switch = FDSwitch(
			icon='',
			title='test')
		cls.app.screen.add_widget(cls.switch)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.switch)

	def test_set_value(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.ids.switch.active, False)

		self.switch.set_value(True)
		self.assertEqual(self.switch.ids.switch.active, True)

	def test_get_value(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.get_value(), False)

		self.switch.set_value(True)
		self.assertEqual(self.switch.get_value(), True)

	def test_set_value_none(self):
		self.assertRaises(ValueError, lambda: self.switch.set_value(None))


class TestFDDoubleSwitch(unittest.TestCase):
	''' Тесты FDDoubleSwitch '''

	@classmethod
	def setUpClass(cls):
		cls.app = AppTest()
		cls.active_icon = 'bus'
		cls.deactive_icon = 'account'
		cls.active_title = 'active'
		cls.deactive_title = 'deactive'
		cls.switch = FDDoubleSwitch(
			icon_active=cls.active_icon,
			icon_deactive=cls.deactive_icon,
			title_active='active',
			title_deactive='deactive',
		)
		cls.app.screen.add_widget(cls.switch)

	@classmethod
	def tearDownClass(cls):
		cls.app.screen.remove_widget(cls.switch)

	def test_set_value(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.ids.switch.active, False)

		self.switch.set_value(True)
		self.assertEqual(self.switch.ids.switch.active, True)

	def test_get_value(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.get_value(), False)

		self.switch.set_value(True)
		self.assertEqual(self.switch.get_value(), True)

	def test_set_value_none(self):
		self.assertRaises(ValueError, lambda: self.switch.set_value(None))

	def test_icons(self):
		self.switch.set_value(True)
		self.assertEqual(self.switch.ids.icon.icon, self.active_icon)

		self.switch.set_value(False)
		self.assertEqual(self.switch.ids.icon.icon, self.deactive_icon)

	def test_titles(self):
		self.switch.set_value(True)
		self.assertEqual(self.switch.ids.title.text, self.active_title)

		self.switch.set_value(False)
		self.assertEqual(self.switch.ids.title.text, self.deactive_title)


if __name__ == '__main__':
	unittest.main()
