from django.shortcuts import render_to_response, get_object_or_404

from photos.models import Photo, Album
from profiles.models import User
from photos.serializers import PhotoSerializer

import json
import hashlib


def show(request, username):
    user = get_object_or_404(User, profile_name=username)
    photos = Photo.objects.filter(user=user)
    serializer = PhotoSerializer(photos, many=True)
    photos_hash = {
        'photos': json.dumps(serializer.data),
        'albums': Album.objects.filter(user=user),
        'username': username,
        'gravatar': hashlib.md5(user.email.lower().encode('utf-8')).hexdigest()
    }
    return render_to_response('profiles/show.html', photos_hash)
