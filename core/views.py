from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from photos.serializers import PhotoSerializer
from photos.models import Photo

import json


@login_required
def root(request):
    photos = Photo.objects.all()[:40]
    serializer = PhotoSerializer(photos, many=True)
    photos = json.dumps(serializer.data)
    return render_to_response('core/index.html', {'photos': photos})
