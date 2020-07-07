from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """Test that user can be created with email"""
        email = 'test@email.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_user_email(self):
        """Test that email is normalized when creating user"""
        email = 'test@EmAIl.COm'
        user = get_user_model().objects.create_user(
            email,
            'testpass'
        )
        self.assertEqual(user.email, email.lower())

    def test_create_user_invalid_email(self):
        """Test that creating user with invalid email fails"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'testpass'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
