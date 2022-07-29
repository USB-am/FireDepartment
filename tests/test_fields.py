import unittest

from main import Application
from app.tools.fields.controllers import FDSwitch
from app.tools.fields.selected_list import SelectedList, ListElement


app = Application()


class TestFDSwitch(unittest.TestCase):
	def setUp(self):
		self.switch = FDSwitch('Human')

	def test_getter_setter(self):
		self.assertFalse(self.switch.get_value(), False)

		self.switch.set_value(True)
		self.assertTrue(self.switch.get_value(), True)


class TestSelectedList(unittest.TestCase):
	def setUp(self):
		self.group_list = SelectedList(icon='wrench', title='Human', group='group_1')
		self.multi_list = SelectedList(icon='wrench', title='Human')

	def test_group_update_content(self):
		values = [f'Value #{i+1}' for i in range(100)]

		self.group_list.update_content(values)
		group_content = self.group_list.ids.content

		self.assertEqual(len(group_content.children), 100)
		self.assertIsInstance(group_content.children[0], ListElement)

	def test_multi_update_content(self):
		values = [f'Value #{i+1}' for i in range(100)]

		self.multi_list.update_content(values)
		multi_content = self.multi_list.ids.content

		self.assertEqual(len(multi_content.children), 100)
		self.assertIsInstance(multi_content.children[0], ListElement)


if __name__ == '__main__':
	unittest.main()