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
        self.user = user

    def store_and_save_photos(self):
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        bucket = conn.get_bucket(settings.AWS_IMAGE_BUCKET, validate=False)
        k = Key(bucket)
        k.key = 'images/'+self.user.username[0]+'/'+self.user.username[1:]+'/'+self.uploaded_file.name
        k.set_contents_from_file(self.uploaded_file)
        original_file_path = settings.AWS_IMAGE_BUCKET + '/' + k.key

        dirs_path = 'tmp/'+self.user.username+'/'
        if not os.path.exists(dirs_path): os.makedirs(dirs_path)
        tmp_path = dirs_path + self.uploaded_file.name
        with open(tmp_path, 'wb+') as destination:
            for chunk in self.uploaded_file.chunks():
                destination.write(chunk)

        img = Image.open(tmp_path)

        exifinfo = img._getexif()

        os.remove(tmp_path)

        exif_dict = {
            'ISOSpeedRatings': None,
            'Make': None,
            'Model': None,
            'LensModel': None,
            'FNumber': (None, None),
            'FocalLength': (None, None),
        }
        if exifinfo:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                exif_dict[decoded] = value
        exif_info = exif_dict

        return Photo.objects.create(
            url='//s3.amazonaws.com/' + original_file_path,
            size=self.uploaded_file.size,
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
