from django import forms

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class ImageUploader(object):
    def upload_image(file):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET)
        k = Key(bucket)
        k.key = 'images/'+request.user.username+'/'+filename
        k.set_contents_from_file(resized_photo)


class ImageUploadForm(forms.Form):
    image = forms.FileField()

    # def __init__(self, *args, **kwargs):
    #     if request.FILES:
    #         image_uploader = ImageUploader()
    #         for file in request.FILES:
    #             image_uploader.upload_image(file)
