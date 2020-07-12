from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from vendor.models import Vendor
from vendor.serializers import VendorSerializer


VENDOR_URL = reverse('vendor:vendor-list')
VENDOR_DETAIL_URL = reverse('vendor:me')


sample_vendor_count = 0


def sample_vendor(user=None, name='Sample Vendor'):
    global sample_vendor_count
    if not user:
        user = get_user_model().objects.create_user(
            f'test{sample_vendor_count}@email.com',
            'testpass'
        )
        sample_vendor_count += 1
    return Vendor.objects.create(
        user=user,
        name=name
    )


class PublicVendorApiTests(TestCase):
    """Test unauthenticated vendor API access"""

    def setUp(self):
        self.client = APIClient()

    def test_list_vendors(self):
        """Test retrieving the list of vendors"""
        sample_vendor()
        sample_vendor()

        req = self.client.get(VENDOR_URL)

        vendors = Vendor.objects.all().order_by('id')
        serializer = VendorSerializer(vendors, many=True)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.data, serializer.data)

    def test_create_fails(self):
        """Test that creation fails while unauthorized"""
        req = self.client.post(VENDOR_URL, {})
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_vendor_update_denied(self):
        """Test that updating vendor denied while unauthorized"""
        req = self.client.get(VENDOR_DETAIL_URL)
        self.assertEqual(req.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateVendorApiTests(TestCase):
    """Test authenticated vendor API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_create_vendor(self):
        """Test creating a vendor for the authenticated user"""
        payload = {
            'name': 'Test Vendor'
        }
        req = self.client.post(VENDOR_URL, payload)

        self.assertEqual(req.status_code, status.HTTP_201_CREATED)

        vendor = Vendor.objects.get(id=req.data['id'])
        for key in payload:
            self.assertEqual(payload[key], getattr(vendor, key))
        self.assertEqual(self.user.vendor.id, req.data['id'])

    def test_vendor_detail_view(self):
        """Test access to vendor detail view"""
        vendor = sample_vendor(user=self.user, name='test_vendor_detail_view')

        req = self.client.get(VENDOR_DETAIL_URL)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.data, {
            'id': vendor.id,
            'name': vendor.name
        })

    def test_vendor_detail_returns_user_vendor(self):
        """Test that the vendor detail returns the authenticated user's vendor"""
        sample_vendor(name='Not my vendor')
        vendor = sample_vendor(user=self.user, name='My Vendor')
        sample_vendor(name='Also not my vendor')

        req = self.client.get(VENDOR_DETAIL_URL)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(req.data, {
            'id': vendor.id,
            'name': vendor.name
        })
