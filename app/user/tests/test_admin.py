from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            'admin@email.com',
            'securepass'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )

    def test_list_users(self):
        """Test users are listed on the user page"""
        url = reverse('admin:user_user_changelist')
        req = self.client.get(url)

        self.assertContains(req, self.user.name)
        self.assertContains(req, self.user.email)

    def test_load_edit_user(self):
        """Test that the edit user page loads"""
        url = reverse('admin:user_user_change', args=[self.user.id])
        req = self.client.get(url)

        self.assertEqual(req.status_code, 200)

    def test_load_add_user(self):
        """Test that the add user page loads"""
        url = reverse('admin:user_user_add')
        req = self.client.get(url)

        self.assertEqual(req.status_code, 200)
