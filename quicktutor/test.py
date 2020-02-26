from django.test import TestCase
import unittest

class MyTestCase(unittest.TestCase):
	def test_list_int(self):
  		data = [1, 2, 3]
  		result = sum(data)
  		self.assertEqual(result, 6)