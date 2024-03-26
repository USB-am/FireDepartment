import unittest

from call_manager import PhoneProperty
from ui.widgets.triple_checkbox import FDTripleCheckbox


class TestPhoneProperty(unittest.TestCase):
	''' Тесты PhoneProperty '''

	custom_property = PhoneProperty(str)

	@classmethod
	def setUpClass(cls):
		self.custom_property = 'Test'

	def test_property_set(self):
		self.assertRaises(TypeError,
		                  lambda: self.custom_property.__set__(self, 1))
