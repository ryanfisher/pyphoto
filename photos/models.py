from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel

class Photo(TimeStampedModel):
    """
    A user's photo
    """
    url = models.URLField(unique=True)
    thumbnail_url = models.URLField()
    original_filename = models.CharField(max_length=255)
    iso = models.IntegerField(null=True)
    size = models.FloatField()
    user = models.ForeignKey(User)
    camera_make = models.CharField(max_length=32, null=True)
    camera_model = models.CharField(max_length=128, null=True)
    lens_model = models.CharField(max_length=128, null=True)
    f_stop_denominator = models.IntegerField(null=True)
    f_stop_numerator = models.IntegerField(null=True)
    exposure_denominator = models.IntegerField(null=True)
    exposure_numerator = models.IntegerField(null=True)
    focal_length_denominator = models.IntegerField(null=True)
    focal_length_numerator = models.IntegerField(null=True)

    def shutter_speed(self):
        numerator = self.exposure_numerator
        denominator = self.exposure_denominator
        if denominator == 0:
            return str(numerator)
        else:
            return str(numerator) + '/' + str(denominator)

    def f_stop(self):
        aperture = float(self.f_stop_numerator) / self.f_stop_denominator
        return format(aperture, '.2f').rstrip('0').rstrip('.')

    class Meta:
        ordering = ['-created']
