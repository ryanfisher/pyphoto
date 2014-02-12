from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel

class Photo(TimeStampedModel):
    """
    A user's photo
    """
    url = models.URLField()
    iso = models.IntegerField()
    size = models.FloatField()
    user = models.ForeignKey(User)
