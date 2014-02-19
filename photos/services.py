from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from PIL import Image
from PIL.ExifTags import TAGS

class PhotoService(object):

    def __init__(self, file):
        self.file = file

    def get_exif(self):
        img = Image.open(self.file)
        exifinfo = img._getexif()
        exif_dict = {}
        for tag, value in exifinfo.items():
            decoded = TAGS.get(tag, tag)
            exif_dict[decoded] = value
        return exif_dict

    def upload_photo(self, folder):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET, validate=False)
        k = Key(bucket)
        k.key = 'images/'+folder+'/'+self.file.name
        k.set_contents_from_file(self.file)
        return '/' + k.key
