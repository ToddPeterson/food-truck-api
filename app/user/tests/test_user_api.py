from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApi(TestCase):
    """Test unauthorized User API access"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a user with valid payload"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass'
        }

        req = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**req.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', req.data)

    def test_create_user_already_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpass'
        }
        create_user(**payload)

        req = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that create user fails when password too short (< 8)"""
        payload = {
            'email': 'test@email.com',
            'password': '1234567'
        }
        req = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token(self):
        """Test creating a token for a user"""
        payload = {
            'email': 'test@email.com',
            'password': 'testpassword'
        }
        create_user(**payload)

        req = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', req.data)
        self.assertEqual(req.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_user(self):
        """Test that token creation fails for invalid credentials"""
        create_user(
            email="test@email.com",
            password="testpassword"
        )
        payload = {
            'email': 'test@email.com',
            'password': 'wrongpass'
        }
        req = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', req.data)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token creation fails if user doesn't exist"""
        payload = {
            'email': 'fake@email.com',
            'password': 'letmein'
        }
        req = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', req.data)
        self.assertEqual(req.status_code, status.HTTP_400_BAD_REQUEST)
