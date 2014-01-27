from django.shortcuts import redirect, render_to_response
from django.conf import settings

from django.contrib.auth.decorators import login_required

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import logging

class ImageUploader(object):
    def upload_image(file):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET)
        k = Key(bucket)
        k.key = 'images/'+request.user.username+'/'+filename
        k.set_contents_from_file(resized_photo)

@login_required
def upload(request):
    if request.method == 'GET':
        return render_to_response('photos/upload.html')
    elif request.method == 'POST':
        if request.FILES:
            image_uploader = ImageUploader()
            for file in request.FILES:
                image_uploader.upload_image(file)
        return redirect('/')
