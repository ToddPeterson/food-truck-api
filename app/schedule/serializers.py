from rest_framework import serializers

from schedule.models import Location


class LocationSerializer(serializers.Serializer):
    """Serializer for a location object"""

    class Meta:
        model = Location
        fields = ('id', 'name', 'info', 'longitude', 'latitude')
        read_only_fields = ('id',)
