from django.test import TestCase
from django.contrib.auth import get_user_model

from schedule.models import Location
from vendor.models import Vendor


_sample_vendor_count = 0


def sample_vendor(user=None, name='Sample Vendor'):
    global _sample_vendor_count
    if not user:
        user = get_user_model().objects.create_user(
            f'test{_sample_vendor_count}@email.com',
            'testpass'
        )
        _sample_vendor_count += 1
    return Vendor.objects.create(
        user=user,
        name=name
    )


class LocationTests(TestCase):

    def test_create_location(self):
        """Test creating a location"""
        vendor = sample_vendor()
        location = Location.objects.create(
            vendor=vendor,
            name='New location',
            info='Words words words',
            longitude=1.23,
            latitude=4.56
        )

        self.assertEqual(location.vendor.id, vendor.id)
        self.assertEqual(location.name, 'New location')
        self.assertEqual(location.info, 'Words words words')
        self.assertEqual(location.longitude, 1.23)
        self.assertEqual(location.latitude, 4.56)

    def test_location_str(self):
        """Test that location objects return the correct string rep"""
        vendor = sample_vendor()
        location = Location.objects.create(
            vendor=vendor,
            name='New location',
            info='Words words words',
            longitude=1.23,
            latitude=4.56
        )

        expected = f'{location.name}::{location.longitude},{location.latitude}'
        self.assertEqual(str(location), expected)
