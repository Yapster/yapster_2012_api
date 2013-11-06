import json

from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from provider.oauth2.models import Client as OAuth2Client


class APITest(TestCase):
    c = Client()

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

        User.objects.create_user(
            'test', 'test@test.com', 'test')

        response = self.c.post('/oauth2/access_token/', {
            'grant_type': 'password',
            'client_id': '28ef4b72f407244ce99f',
            'client_secret': 'c0bf3724ed65f2d91d84a55e8b90afe4c34f43dc',
            'username': 'test',
            'password': 'test',
        })
        access_token = json.loads(response.content)['access_token']
        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token
        }

    def test_yap(self):
        data = {
            "title": "123",
            "path": "123",
            "length": "123",
            "tagstr": "123"
        }
        r = self.c.post('/api/.1/yap/create/',
                        data,
                        **self.auth_headers)
        self.assertEqual(r.status_code, 201, r.content)
