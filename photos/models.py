from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel

class Photo(TimeStampedModel):
    """
    A user's photo
    """
    url = models.URLField(unique=True)
    iso = models.IntegerField(null=True)
    size = models.FloatField()
    user = models.ForeignKey(User)
    camera_make = models.CharField(max_length=32, null=True)
    camera_model = models.CharField(max_length=128, null=True)
    lens_model = models.CharField(max_length=128, null=True)
    f_stop_denominator = models.IntegerField(null=True)
    f_stop_numerator = models.IntegerField(null=True)
    focal_length_denominator = models.IntegerField(null=True)
    focal_length_numerator = models.IntegerField(null=True)
