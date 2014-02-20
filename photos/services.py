from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from PIL import Image
from PIL.ExifTags import TAGS

import os

from photos.models import Photo

class PhotoService(object):

    def __init__(self, uploaded_file, user):
        self.uploaded_file = uploaded_file
        self.size = self.uploaded_file.size
        self.user = user
        self.tmp_path = None

    def tmp_write_to_system(self):
        path = 'tmp/'+self.user.username+'/'
        if not os.path.exists(path): os.makedirs(path)
        self.tmp_path = path + self.uploaded_file.name
        with open(self.tmp_path, 'wb+') as destination:
            for chunk in self.uploaded_file.chunks():
                destination.write(chunk)

    def rm_tmp_file(self):
        if not self.tmp_path: return
        os.remove(self.tmp_path)
        self.tmp_path = None

    def get_exif(self):
        if not self.tmp_path: self.tmp_write_to_system()
        img = Image.open(self.tmp_path)
        exifinfo = img._getexif()
        exif_dict = {
            'ISOSpeedRatings': None,
            'Make': None,
            'Model': None,
            'LensModel': None,
            'FNumber': (None, None),
            'FocalLength': (None, None),
        }
        if not exifinfo: return exif_dict
        for tag, value in exifinfo.items():
            decoded = TAGS.get(tag, tag)
            exif_dict[decoded] = value
        return exif_dict

    def upload_photo(self, folder):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET, validate=False)
        k = Key(bucket)
        k.key = 'images/'+folder+'/'+self.uploaded_file.name
        k.set_contents_from_file(self.uploaded_file)
        return '/' + k.key

    def store_photo(self):
        path = self.upload_photo(self.user.username)
        path = settings.AWS_IMAGE_BUCKET + path
        exif_info = self.get_exif()
        self.rm_tmp_file()
        return Photo.objects.create(
            url='//s3.amazonaws.com/' + path,
            size=self.size,
            iso=exif_info['ISOSpeedRatings'],
            user=self.user,
            camera_make=exif_info['Make'],
            camera_model=exif_info['Model'],
            lens_model=exif_info['LensModel'],
            f_stop_numerator=exif_info['FNumber'][0],
            f_stop_denominator=exif_info['FNumber'][1],
            focal_length_numerator=exif_info['FocalLength'][0],
            focal_length_denominator=exif_info['FocalLength'][1]
        )
