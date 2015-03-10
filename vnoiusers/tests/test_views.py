from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory
from vnoiusers import views

# ===============================user_profile==============

def create_user(username, password):
	return User.objects.create(username = username, password = password)

def update_user_info(user_id, firstname, email):
	user = User.objects.get(pk = user_id)
	user.firstname = firstname
	user.email = email

class UserViewTest(TestCase):

	fixtures = ['forum.json', 'auth.json']

	def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

	def test_display_profile_wrongID(self):
		count = User.objects.count()
		response = self.client.get(reverse('vnoiusers:user_profile', kwargs={'user_id':0}))
		self.assertEqual(response.status_code, 200)