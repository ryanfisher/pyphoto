from rest_framework import serializers
from photos.models import Photo, Album


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            'id',
            'optimized_url',
            'thumbnail_url',
            'height',
            'width',
            'iso',
            'camera_make',
            'camera_model',
            'lens_model',
        )


class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)

    class Meta:
        model = Album
        fields = ('id', 'title', 'photos')
