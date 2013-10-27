import json
from django.test import TestCase
from django.test import Client
from provider.oauth2.models import Client as OAuth2Client


class APITest(TestCase):
    c = Client()

    user1_data = {
        'username': 'xinzhou',
        'email': 'xinzhou918@yapster.com',
        'password': 'xinzhou'
    }
    user2_data = {
        'username': 'johnqiao',
        'email': 'johnqiao@yapster.com',
        'password': 'johnqiao'
    }

    def setUp(self):
        # client add
        c = OAuth2Client()
        c.client_id = '28ef4b72f407244ce99f'
        c.client_secret = 'c0bf3724ed65f2d91d84a55e8b90afe4c34f43dc'
        c.name = 'yapster'
        c.url = 'http://localhost/'
        c.client_type = 1
        c.redirect_uri = "http://localhost/"
        c.user_id = 1
        c.save()

        # register user
        self.c.post(
            '/api/.1/accounts/register/', self.user1_data)
        self.c.post(
            '/api/.1/accounts/register/', self.user2_data)

    def test_access_token(self):
        response = self.c.post('/oauth2/access_token/', {
            'grant_type': 'password',
            'client_id': '28ef4b72f407244ce99f',
            'client_secret': 'c0bf3724ed65f2d91d84a55e8b90afe4c34f43dc',
            'username': 'xinzhou',
            'password': 'xinzhou',
        })
        self.assertEqual(200, response.status_code, response.content)
        self.assertIn('access_token', json.loads(response.content))
