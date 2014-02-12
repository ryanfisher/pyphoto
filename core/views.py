from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from photos.models import Photo

@login_required
def root(request):
    photos = Photo.objects.filter(user=request.user)
    return render_to_response('core/index.html', {'photos': photos})
