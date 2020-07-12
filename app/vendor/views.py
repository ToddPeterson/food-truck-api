from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from vendor import serializers
from vendor.models import Vendor


class VendorViewSet(viewsets.ModelViewSet):
    """Manage Vendors in the database"""

    serializer_class = serializers.VendorSerializer
    queryset = Vendor.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """Create a new vendor"""
        serializer.save(user=self.request.user)


class ManageVendorView(generics.RetrieveUpdateAPIView):
    """Manage the vendor associated with the authenticated user"""

    serializer_class = serializers.VendorSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve the vendor associated with the authenticated user"""
        return self.request.user.vendor
