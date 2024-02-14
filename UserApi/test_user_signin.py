from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        user = {
            "username" : 'user1',
            "password" : 'xyz',
        }
        response = self.client.post(reverse('user-list'), user, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'user1')
        self.assertNotIn('password', response.data) #Password must not be here in response
        self.assertIn('access', response.data)  # Check if 'access' token is present

    def test_existing_user(self):
        user = {
            "username" : 'user1',
            "password" : 'xyz',
        }
        response = self.client.post(reverse('user-list'), user, format='json')
        response = self.client.post(reverse('user-list'), user, format='json')

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')
        self.assertNotIn('password', response.data) #Password must not be here in response
        self.assertIn('access', response.data)  # Check if 'access' token is present

    def test_null_username_password(self):
        user = {
            "username" : '',
            "password" : 'xyz',
        }
        response = self.client.post(reverse('user-list'), user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user = {
            "username" : 'user1',
            "password" : '',
        }
        response = self.client.post(reverse('user-list'), user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

