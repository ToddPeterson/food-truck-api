from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from schedule import serializers
from schedule.models import Location


class LocationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Viewset for user owned location entities"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer

    def get_queryset(self):
        """Return locations for the current authenticated user"""
        return self.queryset.filter(
            vendor=self.request.user.vendor
        ).order_by('-id').distinct()
