from django.test import TestCase
from django.test import Client

from django.contrib.auth.models import User


class APITest(TestCase):
    c = Client()
    data = {
        'username': 'xinzhou',
        'email': 'xinzhou918@gmail.com',
        'password': 'xinzhou'
    }

    def test_register(self):
        response = self.c.post(
            '/api/.1/accounts/register/', self.data)
        self.assertEqual(response.status_code, 200)

        u = User.objects.get(username='xinzhou')
        self.assertEqual(u.email, 'xinzhou918@gmail.com')
        self.assertTrue(u.check_password('xinzhou'))
        self.assertTrue(u.info)
        self.assertTrue(u.setting)

    def test_register_fail(self):
        response = self.c.post(
            '/api/.1/accounts/register/', {})
        self.assertEqual(response.status_code, 400)

    def test_register_dupl(self):

        response = self.c.post(
            '/api/.1/accounts/register/', self.data)
        self.assertEqual(response.status_code, 200)

        u = User.objects.get(username='xinzhou')
        self.assertEqual(u.email, 'xinzhou918@gmail.com')
        self.assertTrue(u.check_password('xinzhou'))

        response = self.c.post(
            '/api/.1/accounts/register/', self.data)
        self.assertEqual(response.status_code, 400)
