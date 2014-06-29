from rest_framework import serializers
from photos.models import Photo, Album


class PhotoSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('profile_user')
    taken = serializers.SerializerMethodField('date_taken')

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
            'taken',
            'lens_model',
            'username',
        )

    def date_taken(self, obj):
        return str(obj.date_taken)

    def profile_user(self, obj):
        return obj.user.profile_name


class AlbumSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField('sorted_photos')

    class Meta:
        model = Album
        fields = ('id', 'title', 'photos')

    def sorted_photos(self, obj):
        photos_by_position = obj.photos.order_by('sortedphoto__position')
        return [PhotoSerializer(photo).data for photo in photos_by_position]
