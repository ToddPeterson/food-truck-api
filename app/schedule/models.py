from django.db import models


class Location(models.Model):
    """Model representing a schedule location"""

    name = models.CharField(max_length=255, blank=True)
    info = models.CharField(max_length=255, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    vendor = models.ForeignKey(
        'vendor.Vendor',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}::{self.longitude},{self.latitude}'


class Event(models.Model):
    """Model representing a schedule event"""

    name = models.CharField(max_length=255, blank=True)
    info = models.CharField(max_length=255, blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    location = models.ForeignKey(
        'schedule.Location',
        on_delete=models.CASCADE
    )
    vendor = models.ForeignKey(
        'vendor.Vendor',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.date_start.date}::{self.location.name}'
