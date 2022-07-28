import unittest

from main import Application
from app.tools.fields.controllers import FDSwitch
from app.tools.fields.selected_list import SelectedList


app = Application()


class TestFDSwitch(unittest.TestCase):
	def setUp(self):
		self.switch = FDSwitch('Human')

	def test_getter_setter(self):
		self.assertEqual(self.switch.get_value(), False)

		self.switch.set_value(True)
		self.assertEqual(self.switch.get_value(), True)


class TestFields(unittest.TestCase):
	def setUp(self):
		group_list = SelectedList(icon='wrench', title='Human', group='group_1')


if __name__ == '__main__':
	unittest.main()