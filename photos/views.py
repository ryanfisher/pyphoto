from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from photos import forms
from photos.models import Photo

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class ImageUploader(object):

    @staticmethod
    def upload_image(file, folder):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET, validate=False)
        k = Key(bucket)
        k.key = 'images/'+folder+'/'+file.name
        k.set_contents_from_file(file)
        return '/' + k.key

@login_required
def upload(request):
    if request.method == 'GET':
        image_form = forms.ImageUploadForm()
        return render_to_response(
            'photos/upload.html',
            {'form': image_form},
            context_instance=RequestContext(request)
        )
    elif request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['file']
            path = ImageUploader().upload_image(image_file, request.user.username)
            path = settings.AWS_IMAGE_BUCKET + path
            Photo.objects.create(
                url='//s3.amazonaws.com/' + path,
                size=image_file.size,
                iso=100,
                user=request.user
            )
        return redirect('/')
