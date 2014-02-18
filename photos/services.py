from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class PhotoService(object):

    def __init__(self):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        self.bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET, validate=False)

    def upload_photo(self, file, folder):
        k = Key(self.bucket)
        k.key = 'images/'+folder+'/'+file.name
        k.set_contents_from_file(file)
        return '/' + k.key
