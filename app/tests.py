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
		self.assertTrue(client.login(username='mamba@gmail.com', password='CS3240!!'), 'Login unsuccessful.')


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
			self.assertEqual(response.templates[0].name, 'app/index.html', 'User was able to access restricted page without logging in.')

	def test_navigation_after_login(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Accessing base URL redirects them to feed page
		response = client.get('/', follow=True)
		self.assertEqual(response.templates[0].name, 'app/feed.html', 'Base URL did not redirect to feed page.')

		# Accessing any other URL brings them to corresponding page
		urls = ['/', '/feed/', '/myRequest/', '/profile/', '/contacts/', '/messages/']
		page_names = ['', 'feed', 'myRequest', 'profile', 'contacts', 'messages']  # no slashes for concatenation purposes

		for i in range(1, len(urls)):  # don't want to include the base URL... so start index at 1
			response = client.get(urls[i], follow=True)
			name = 'app/' + page_names[i] + '.html'
			self.assertEqual(response.templates[0].name, name, 'Could not access ' + page_names[i] + ' page.')


class RequestTestCases(TestCase):
	# Create a user before tests and post a request
	def setUp(self):
		# Create user
		User.objects.create_user('mamba@gmail.com', 'CS3240!!')
		User.objects.create_user('mamba@yahoo.com', 'password')

	# Check that user's boolean is set when they create a request
	def test_has_active_request(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		response = client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
											   'description': 'I really need help. $5'}, follow=True)

		user = User.objects.get(email='mamba@gmail.com')
		self.assertTrue(user.has_active_request, 'has_active_request boolean was not set.')

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
		self.assertEqual(request.title, 'Help me!', 'Title does not match.')
		self.assertEqual(request.location, 'Clark', 'Location does not match.')
		self.assertEqual(request.description, 'I really need help. $5', 'Description does not match.')

	# Check that a user can't create two requests via two POST requests
	def test_second_request(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST requests to myRequest page to try to create two new requests
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
									'description': 'I really need help. $5'}, follow=True)

		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help', 'location': 'Clem',
									'description': 'Please.'}, follow=True)

		# Get user
		user = User.objects.get(email='mamba@gmail.com')

		# See if the second request was created
		request_search = Request.objects.filter(user=user.email)

		# Should be of length 1
		self.assertEqual(len(request_search), 1, 'User has two active requests.')

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

		self.assertEqual(len(request_search), 0, 'Deletion failed; user still has active request.')
		self.assertFalse(user.has_active_request, 'has_active_request boolean was not set to false.')

	# When a user edits a request, make sure that they are taken to request editor with their own request info
	# filled in
	def test_request_editor_rendered(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
									'description': 'I really need help. $5'}, follow=True)

		# Send POST request to myRequest page to edit request
		response = client.post('/myRequest/', {'action': 'Edit'}, follow=True)

		# Context should be filled with the user's request data
		title = response.context['title']
		location = response.context['location']
		description = response.context['description']

		self.assertEqual(title, 'Help me!', 'Title does not match.')
		self.assertEqual(location, 'Clark', 'Location does not match.')
		self.assertEqual(description, 'I really need help. $5', 'Description does not match.')

		# Should have rendered the request editor template 'app/requestEditor.html'
		template = response.templates[0].name
		self.assertEqual(template, 'app/requestEditor.html', 'Request editor template was not rendered.')

	# When a user updates a request with new information via the request editor page, check that the request
	# is actually updated with the new data.
	def test_request_update(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
									'description': 'I really need help. $5'}, follow=True)

		# Send POST request to myRequest page to edit request
		client.post('/myRequest/', {'action': 'Edit'}, follow=True)

		# Send POST request to myRequest page to update the request
		response = client.post('/myRequest/', {'action': 'Update', 'title': 'New title!', 'location': 'New location!',
											   'description': 'New description!'}, follow=True)

		# Get user
		user = User.objects.get(email='mamba@gmail.com')

		# See if their request has been updated with the new info
		request = Request.objects.filter(user=user.email)[0]
		self.assertEqual('New title!', request.title, 'Title does not match.')
		self.assertEqual('New location!', request.location, 'Location does not match.')
		self.assertEqual('New description!', request.description, 'Description does not match.')

	# Make sure that when two different users create requests, accessing myRequest page displays correct one.
	def test_multiple_users_and_requests(self):
		# Create client and login
		client = Client()
		client.login(username='mamba@gmail.com', password='CS3240!!')

		# Send POST request to myRequest page to create a new request
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me!', 'location': 'Clark',
									'description': 'I really need help. $5'}, follow=True)

		# Login as other user and create second request
		client.login(username='mamba@yahoo.com', password='password')
		client.post('/myRequest/', {'action': 'Submit', 'title': 'Help me 2!', 'location': 'Clem',
									'description': 'I really need help. $10'}, follow=True)

		# Check myRequest page for the correct request
		response = client.get('/myRequest/')
		request = response.context['request']

		self.assertEqual('Help me 2!', request.title, 'Title does not match.')
		self.assertEqual('Clem', request.location, 'Location does not match.')
		self.assertEqual('I really need help. $10', request.description, 'Description does not match.')

		# Login as first user and check myRequest page for their request
		client.login(username='mamba@gmail.com', password='CS3240!!')
		response = client.get('/myRequest/')
		request = response.context['request']

		self.assertEqual('Help me!', request.title, 'Title does not match.')
		self.assertEqual('Clark', request.location, 'Location does not match.')
		self.assertEqual('I really need help. $5', request.description, 'Description does not match.')