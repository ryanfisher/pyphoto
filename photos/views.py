from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from photos import forms

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class ImageUploader(object):

    @staticmethod
    def upload_image(file):
        user_name = 'ryanfisher'

        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET)
        k = Key(bucket)
        k.key = 'images/'+user_name+'/'+file.name
        k.set_contents_from_file(file)

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
            ImageUploader().upload_image(request.FILES['file'])
        return redirect('/')
