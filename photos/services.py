from django.conf import settings

from boto.s3.connection import S3Connection
from PIL import Image
from PIL.ExifTags import TAGS
from cStringIO import StringIO

import os

from photos.models import Photo

THUMBNAIL_SIZE = 600
OPTIMIZED_WIDTH = 1800
OPTIMIZED_HEIGHT = 1200


class TemporaryImageFile(object):
    def __init__(self, uploaded_file):
        random_folder = 'random'
        dirs_path = 'tmp/'+random_folder+'/'
        if not os.path.exists(dirs_path):
            os.makedirs(dirs_path)
        self.path = dirs_path + uploaded_file.name
        with open(self.path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

    def delete(self):
        os.remove(self.path)


class PhotoService(object):

    def __init__(self, uploaded_file, user):
        self.uploaded_file = uploaded_file
        self.user = user
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        self.bucket = conn.get_bucket(
            settings.AWS_IMAGE_BUCKET,
            validate=False
        )

    def send_to_s3(self, file, file_prefix=""):
        hashed_dirs = self.user.username[0]+'/'+self.user.username[1:]+'/'
        file_key = 'images/'+hashed_dirs+file_prefix+self.uploaded_file.name
        k = self.bucket.new_key(file_key)
        k.set_contents_from_file(file, replace=False)
        return settings.AWS_IMAGE_BUCKET + '/' + k.key

    def send_string_to_s3(self, string_file, file_prefix="thumbnail_"):
        hashed_dirs = self.user.username[0]+'/'+self.user.username[1:]+'/'
        file_key = 'images/'+hashed_dirs+file_prefix+self.uploaded_file.name
        k = self.bucket.new_key(file_key)
        k.set_contents_from_string(
            string_file,
            headers={"Content-Type": "image/jpeg"}
        )
        return settings.AWS_IMAGE_BUCKET + '/' + k.key

    def create_and_store_thumbnail(self, img):
        width = THUMBNAIL_SIZE * img.size[0] / img.size[0]
        img.thumbnail((width, THUMBNAIL_SIZE), Image.ANTIALIAS)

        image_string = StringIO()
        img.save(image_string, 'JPEG')

        thumbnail_url = self.send_string_to_s3(image_string.getvalue())

        image_string.close()

        return thumbnail_url

    def create_and_store_optimized(self, img):
        width = OPTIMIZED_HEIGHT * img.size[0] / img.size[0]
        if width < OPTIMIZED_WIDTH:
            height = OPTIMIZED_HEIGHT
        else:
            width = OPTIMIZED_WIDTH
            height = OPTIMIZED_WIDTH * img.size[1] / img.size[1]
        img.thumbnail((width, height), Image.ANTIALIAS)

        image_string = StringIO()
        img.save(image_string, 'JPEG')

        url = self.send_string_to_s3(image_string.getvalue(), 'optimized_')

        image_string.close()

        return url

    def store_and_save_photos(self):
        original_file_path = self.send_to_s3(self.uploaded_file)

        tmp_image = TemporaryImageFile(self.uploaded_file)
        img = Image.open(tmp_image.path)

        exifinfo = img._getexif()

        optimized_url = self.create_and_store_optimized(img)
        thumbnail_url = self.create_and_store_thumbnail(img)

        tmp_image.delete()

        exif_dict = {
            'ISOSpeedRatings': None,
            'Make': None,
            'Model': None,
            'LensModel': None,
            'FNumber': (None, None),
            'FocalLength': (None, None),
            'ExposureTime': (None, None),
        }
        if exifinfo:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                exif_dict[decoded] = value
        exif_info = exif_dict

        return Photo.objects.create(
            original_filename=self.uploaded_file.name,
            url='//s3.amazonaws.com/' + original_file_path,
            optimized_url='//s3.amazonaws.com/' + optimized_url,
            thumbnail_url='//s3.amazonaws.com/' + thumbnail_url,
            size=self.uploaded_file.size,
            iso=exif_info['ISOSpeedRatings'],
            user=self.user,
            camera_make=exif_info['Make'],
            camera_model=exif_info['Model'],
            lens_model=exif_info['LensModel'],
            f_stop_numerator=exif_info['FNumber'][0],
            f_stop_denominator=exif_info['FNumber'][1],
            exposure_numerator=exif_info['ExposureTime'][0],
            exposure_denominator=exif_info['ExposureTime'][1],
            focal_length_numerator=exif_info['FocalLength'][0],
            focal_length_denominator=exif_info['FocalLength'][1]
        )
