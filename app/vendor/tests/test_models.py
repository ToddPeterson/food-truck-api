from django.test import TestCase
from django.contrib.auth import get_user_model

from vendor.models import Vendor


class VendorTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )

    def test_create_vendor(self):
        """Test creating a vendor"""
        name = 'Test Vendor'
        vendor = Vendor.objects.create(
            name=name,
            user=self.user
        )

        self.assertEqual(vendor.name, name)
        self.assertEqual(vendor.user.id, self.user.id)

    def test_vendor_str(self):
        """Test that vendors return the correct string rep"""
        name = 'Test Vendor'
        vendor = Vendor.objects.create(
            name=name,
            user=self.user
        )

        self.assertEqual(str(vendor), name)
