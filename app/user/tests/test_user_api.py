from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


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
