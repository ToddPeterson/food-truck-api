from random import random

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from vendor.models import Vendor
from schedule.models import Location
from schedule.serializers import LocationSerializer


LOCATION_URL = reverse('schedule:location-list')


def sample_location(vendor, name='A Location', info='info'):
    return Location.objects.create(
        vendor=vendor,
        name=name,
        info=info,
        longitude=random() * 100,
        latitude=random() * 100,
    )


class PublicLocationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_public_access_denied(self):
        """Test that unauthorized access is denied"""
        req = self.client.get(LOCATION_URL)
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLocationApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password'
        )
        Vendor.objects.create(user=self.user, name='Test Vendor')
        self.client.force_authenticate(self.user)

    def test_list_locations(self):
        """Test retrieving a list of locations"""
        sample_location(self.user.vendor)
        sample_location(self.user.vendor)
        sample_location(self.user.vendor)

        req = self.client.get(LOCATION_URL)

        locations = Location.objects.all().order_by('-id')
        serializer = LocationSerializer(locations, many=True)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.data, serializer.data)

    def test_list_locations_limited_to_user(self):
        """Test that only the user's locations are returned"""
        other_user = get_user_model().objects.create_user(
            'other@email.com',
            'password'
        )
        other_vendor = Vendor.objects.create(
            user=other_user,
            name="Other Vendor"
        )
        sample_location(self.user.vendor)
        sample_location(other_vendor)

        req = self.client.get(LOCATION_URL)

        locations = Location.objects.filter(vendor=self.user.vendor)
        serializer = LocationSerializer(locations, many=True)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(len(req.data), 1)
        self.assertEqual(req.data, serializer.data)
