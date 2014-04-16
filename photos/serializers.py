from rest_framework import serializers
from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'optimized_url',
            'thumbnail_url',
            'iso',
            'camera_make',
            'camera_model',
            'lens_model',
        )
