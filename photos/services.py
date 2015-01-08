from django.conf import settings

from boto.s3.connection import S3Connection
from PIL import Image
from PIL.ExifTags import TAGS
from io import StringIO

import os
import binascii

import time
from datetime import datetime

from photos.models import Photo

THUMBNAIL_SIZE = 600
OPTIMIZED_WIDTH = 1800
OPTIMIZED_HEIGHT = 1200


class ExifInfo(object):
    def __init__(self, img):
        exifinfo = img._getexif()
        exif_dict = {}
        if exifinfo:
            for tag, value in list(exifinfo.items()):
                decoded = TAGS.get(tag, tag)
                exif_dict[decoded] = value
        self.exif_info = exif_dict

    def model(self):
        return self.exif_info.get('Model')

    def make(self):
        return self.exif_info.get('Make')

    def lens_model(self):
        return self.exif_info.get('LensModel')

    def iso(self):
        return self.exif_info.get('ISOSpeedRatings')

    def date_taken(self):
        """
        '2013:10:19 21:42:54'
        """
        time_string = self.exif_info.get('DateTimeOriginal')
        try:
            strp_time = time.strptime(time_string, "%Y:%m:%d %H:%M:%S")
            date_taken = datetime.fromtimestamp(time.mktime(strp_time))
        except TypeError:
            date_taken = None
        return date_taken

    def focal_length_numerator(self):
        try:
            return self.exif_info.get('FocalLength')[0]
        except:
            return None

    def focal_length_denominator(self):
        try:
            return self.exif_info.get('FocalLength')[1]
        except:
            return None

    def exposure_numerator(self):
        try:
            return self.exif_info.get('ExposureTime')[0]
        except:
            return None

    def exposure_denominator(self):
        try:
            return self.exif_info.get('ExposureTime')[1]
        except:
            return None

    def f_stop_numerator(self):
        try:
            return self.exif_info.get('FNumber')[0]
        except:
            return None

    def f_stop_denominator(self):
        try:
            return self.exif_info.get('FNumber')[1]
        except:
            return None

    def get_dictionary(self):
        return self.exif_info


class TemporaryImageFile(object):
    def __init__(self, uploaded_file):
        random_string = binascii.hexlify(os.urandom(10))
        self.path = 'tmp/' + random_string + uploaded_file.name
        with open(self.path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

    def delete(self):
        os.remove(self.path)


class PhotoService(object):

    def __init__(self, uploaded_file, user):
        self.uploaded_file = uploaded_file
        self.user = user
        self.set_random_folder()
        conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        self.bucket = conn.get_bucket(
            settings.AWS_IMAGE_BUCKET,
            validate=False
        )

    def get_key(self, file_prefix=''):
        return os.path.join(
            'images',
            self.user.profile_name[0],
            self.user.profile_name[1:],
            self.random_folder_name,
            file_prefix + self.uploaded_file.name
        )

    def set_random_folder(self):
        '''Creates a unique folder name for the new photo. Only call once.
        '''
        while True:
            self.random_folder_name = binascii.hexlify(os.urandom(10))
            if Photo.objects.filter(key=self.get_key()).count() == 0:
                break

    def photo_exists(self):
        '''Checks to see if a file exists. Currently only uses file size
        '''
        count = Photo.objects.filter(user=self.user,
                                     size=self.uploaded_file.size).count()
        return count > 0

    def send_to_s3(self, file, file_prefix=""):
        k = self.bucket.new_key(self.get_key(file_prefix))
        headers={"Cache-Control": "max-age=31536000,public"}
        k.set_contents_from_file(file, headers=headers, replace=False)
        return k.key

    def send_string_to_s3(self, string_file, file_prefix="thumbnail_"):
        k = self.bucket.new_key(self.get_key(file_prefix))
        k.set_contents_from_string(
            string_file,
            headers={
                "Content-Type": "image/jpeg",
                "Cache-Control": "max-age=31536000,public"
            },
            replace=False
        )
        return k.key

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

        key = self.send_string_to_s3(image_string.getvalue(), 'optimized_')

        image_string.close()

        return key

    def store_and_save_photos(self):
        key = self.send_to_s3(self.uploaded_file)
        original_file_path = os.path.join(settings.AWS_IMAGE_BUCKET, key)

        tmp_image = TemporaryImageFile(self.uploaded_file)
        img = Image.open(tmp_image.path)

        exifinfo = ExifInfo(img)

        optimized_key = self.create_and_store_optimized(img)
        optimized_url = os.path.join(settings.AWS_IMAGE_BUCKET, optimized_key)
        thumbnail_key = self.create_and_store_thumbnail(img)
        thumbnail_url = os.path.join(settings.AWS_IMAGE_BUCKET, thumbnail_key)

        tmp_image.delete()

        return Photo.objects.create(
            original_filename=self.uploaded_file.name,
            key=key,
            optimized_key=optimized_key,
            thumbnail_key=thumbnail_key,
            url='//s3.amazonaws.com/' + original_file_path,
            optimized_url='//s3.amazonaws.com/' + optimized_url,
            thumbnail_url='//s3.amazonaws.com/' + thumbnail_url,
            width=img.size[0],
            height=img.size[1],
            size=self.uploaded_file.size,
            iso=exifinfo.iso(),
            date_taken=exifinfo.date_taken(),
            user=self.user,
            camera_make=exifinfo.make(),
            camera_model=exifinfo.model(),
            lens_model=exifinfo.lens_model(),
            f_stop_numerator=exifinfo.f_stop_numerator(),
            f_stop_denominator=exifinfo.f_stop_denominator(),
            exposure_numerator=exifinfo.exposure_numerator(),
            exposure_denominator=exifinfo.exposure_denominator(),
            focal_length_numerator=exifinfo.focal_length_numerator(),
            focal_length_denominator=exifinfo.focal_length_denominator()
        )
