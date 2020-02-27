from django.test import TestCase
import unittest
from django.test import Client 

class MyTestCase(unittest.TestCase):
	def setUp(self):
		c = Client()
		response = c.post('/myRequest/',{'title': '1', 'location' : '2', 'description' : '3', 'pub_date' : '4', 'user' : '5'})
		self.assertEqual(response.status_code , 302)

	def test_Feed(self):
		a = Client()
		response_feed = a.post('feed/',{})
		self.assertEqual(response_feed.status_code , 404)
		#Because there is no get Functionality yet, this should return a Not found page. 

	def test_length_of_feed(self):
		b = Client()
		response_redirect = b.get('profile/', follow = True)
		self.assertIsNotNone(response_redirect.redirect_chain)

	def test_list_int(self):
  		data = [1, 2, 3]
  		result = sum(data)
  		self.assertEqual(result, 6)




  		
		