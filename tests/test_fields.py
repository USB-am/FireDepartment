import unittest
from ui.field.switch import FDSwitch, FDDoubleSwitch


class TestFDSwitch(unittest.TestCase):
	''' Тесты FDSwitch '''

	def setUp(self):
		self.switch = FDSwitch()

	def test_set_value_false(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.ids.switch.active, False)

	def test_set_value_true(self):
		self.switch.set_value(True)
		self.assertEqual(self.switch.ids.switch.active, True)

	def test_get_value_false(self):
		self.switch.set_value(False)
		self.assertEqual(self.switch.get_value(), False)

	def test_get_value_true(self):
		self.switch.set_value(True)
		self.assertEqual(self.switch.get_value(), True)


if __name__ == '__main__':
	unittest.main()
