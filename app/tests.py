from django.test import TestCase, Client
import unittest
from .models import *

'''
NOTES | from https://docs.djangoproject.com/en/3.0/topics/testing/tools/

- Use test client to simulate GET and POST requests
- Test client does not need server to be running
- When retrieving pages, remember to specify path (relative) of URL, not the whole domain
- Make a class to group similar tests
- EVERY TEST METHOD MUST START WITH THE WORD 'test'

setUp()
- called before every test function to set up any objects that may be modified by the test

setUpTestData()
- called once at beginning of the test run for class-level setup to create objects that aren't going to be modified

GET requests
- client.get(path, data=None, follow=False)
- data is in form of dictionary
- returns a Response object
- if you set follow to true, it will follow any redirects

**POST requests are pretty much the same. client.post

Response objects
- response.status_code returns the HTTP status of the response
- response.templates returns list of Template instances used to render the final content


'''


# Testing login process
class LoginTestCases(TestCase):
	# Create a user before tests
	def setUp(self):
		User.objects.create_user('mamba@gmail.com', 'CS3240!!')

	def test_login(self):
		client = Client()

		# Test that login is successful
		self.assertTrue(client.login(username='mamba@gmail.com', password='CS3240!!'))


# Testing navigation around website
class NavigationTestCases(TestCase):
	# Create a user before tests
	def setUp(self):
		User.objects.create_user('mamba@gmail.com', 'CS3240!!')

	def test_navigation_before_login(self):
		client = Client()

		# Test that before logging in, accessing any URL brings them to index.html (the login page)
		urls = ['/', '/feed/', '/myRequest/', '/profile/', '/contacts/', '/messages/']
		for url in urls:
			response = client.get(url, follow=True)
			self.assertTrue(response.templates[0].name == 'app/index.html')

	def test_navigation_after_login(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Accessing base URL redirects them to feed page
		response = client.get('/', follow=True)
		self.assertTrue(response.templates[0].name == 'app/feed.html')

		# Accessing any other URL brings them to corresponding page
		urls = ['/', '/feed/', '/myRequest/', '/profile/', '/contacts/', '/messages/']
		page_names = ['', 'feed', 'myRequest', 'profile', 'contacts', 'messages']  # no slashes for concatenation purposes

		for i in range(1, len(urls)):  # don't want to include the base URL... so start index at 1
			response = client.get(urls[i], follow=True)
			name = 'app/' + page_names[i] + '.html'
			self.assertTrue(response.templates[0].name == name)


class RequestTestCases(TestCase):
	# Create a user before tests and post a request
	def setUp(self):
		# Create user
		User.objects.create_user('mamba@gmail.com', 'CS3240!!')

	# Check that user's boolean is set when they create a request
	def test_has_active_request(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		response = client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
											   'description': 'I really need help. $5'}, follow=True)

		user = User.objects.get(email='mamba@gmail.com')
		self.assertTrue(user.has_active_request)

	# Check that user's created request is displayed on myRequest page, with the correct information
	def test_request_creation(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		response = client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
											   'description': 'I really need help. $5'}, follow=True)

		# Send GET request to myRequest page to view your already made request
		response = client.get('/myRequest/', follow=True)
		request = response.context['request']

		# Make sure data matches
		self.assertTrue(request.title == 'Help me!' and request.location == 'Clark' and request.description == 'I really need help. $5')

	# When user deletes request, their boolean should be set back to false, and the Request.objects list should
	# no longer contain the request
	def test_delete_request(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
											   'description': 'I really need help. $5'}, follow=True)

		# Send POST request to myRequest page to delete request
		response = client.post('/myRequest/', {'action': 'Delete'})

		# Get user
		user = User.objects.get(email='mamba@gmail.com')

		# See if their request still exists - should return set of length 0
		request_search = Request.objects.filter(user=user.email)

		self.assertTrue(len(request_search) == 0 and user.has_active_request is False)
