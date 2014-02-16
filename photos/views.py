from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from photos.forms import ImageUploadForm
from photos.models import Photo
from photos.services import ImageService

@login_required
def upload(request):
    if request.method == 'GET':
        image_form = ImageUploadForm()
        return render_to_response(
            'photos/upload.html',
            {'form': image_form},
            context_instance=RequestContext(request)
        )
    elif request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['file']
            path = ImageService().upload_image(image_file, request.user.username)
            path = settings.AWS_IMAGE_BUCKET + path
            Photo.objects.create(
                url='//s3.amazonaws.com/' + path,
                size=image_file.size,
                iso=100,
                user=request.user
            )
        return redirect('/')
