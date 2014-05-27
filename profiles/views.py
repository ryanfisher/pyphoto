from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from photos.models import Photo
from photos.serializers import PhotoSerializer

import json

def show(request, username):
    user = get_object_or_404(User, username=username)
    photos = Photo.objects.filter(user=user)
    serializer = PhotoSerializer(photos, many=True)
    photos = json.dumps(serializer.data)
    photos_hash = {'photos': photos, 'username': username}
    return render_to_response('profiles/show.html', photos_hash)
