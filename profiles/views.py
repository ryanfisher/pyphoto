from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from photos.models import Photo
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
        'username': username,
        'gravatar': hashlib.md5(user.email.lower()).hexdigest()
    }
    return render_to_response('profiles/show.html', photos_hash)
