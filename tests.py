# -*- coding: utf-8 -*-

import unittest


from UI.form import CreateTag


class TestFormCase(unittest.TestCase):
	def test_get_value_create_form_type(self):
		form = CreateTag()
		# form.update_screen()
		values = form.get_value()
		print(values)

		self.assertIsInstance(values, dict)

	def test_get_value_create_form_valid(self):
		form = CreateTag()
		form.update_screen()

		self.assertRaises(ValueError, form.insert_values())

unittest.main()