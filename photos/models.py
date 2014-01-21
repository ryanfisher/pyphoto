from django.db import models

from core.models import TimeStampedModel

class Photo(TimeStampedModel):
    """
    A user's photo
    """
    url = models.URLField()
    iso = models.IntegerField()
