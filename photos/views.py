from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.template import RequestContext

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
            path = PhotoService().upload_photo(request_file, request.user.username)
            path = settings.AWS_IMAGE_BUCKET + path
            Photo.objects.create(
                url='//s3.amazonaws.com/' + path,
                size=request_file.size,
                iso=100,
                user=request.user
            )
        return redirect('/')
