from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from photos.serializers import PhotoSerializer
from photos.models import Photo

import json


@login_required
def root(request):
    if request.user.is_authenticated():
        return redirect('photos.views.index')
    photos = Photo.objects.all()[:40]
    serializer = PhotoSerializer(photos, many=True)
    photos = json.dumps(serializer.data)
    return render_to_response('core/index.html', {'photos': photos})
