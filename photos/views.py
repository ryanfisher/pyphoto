from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.db import IntegrityError

from django.contrib.auth.decorators import login_required

from photos.forms import PhotoUploadForm
from photos.models import Photo
from photos.services import PhotoService

@login_required
def upload(request):
    if request.method == 'GET':
        photo_form = PhotoUploadForm()
        return render_to_response(
            'photos/upload.html',
            {'form': photo_form},
            context_instance=RequestContext(request)
        )
    elif request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request_file = request.FILES['file']
            try:
                # TODO Check for key in model before trying to upload
                PhotoService(request_file, request.user).store_and_save_photos()
            except IntegrityError:
                return HttpResponse(status=422)
        return redirect('/')

@login_required
def index(request):
    photos = Photo.objects.filter(user=request.user)
    return render_to_response('photos/index.html', {'photos': photos})

def show(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render_to_response('photos/show.html', {'photo': photo})
