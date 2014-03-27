import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from photos.services import PhotoService, ExifInfo


class ExifInfoTest(TestCase):

    def setUp(self):
        path = os.path.join(
            os.getcwd(),
            'photos/tests/fixtures/blake-small.jpg'
        )
        img = Image.open(path)
        self.exif_info = ExifInfo(img)

    def test_model(self):
        self.assertEqual(self.exif_info.model(), u'Canon EOS REBEL T3')

    def test_exif(self):
        result = self.exif_info.get_dictionary()
        self.assertEqual(result['ExposureTime'], (1, 100))
        self.assertEqual(result['FNumber'], (5, 1))
        self.assertEqual(result['ISOSpeedRatings'], 800)
        self.assertEqual(result['FocalLength'], (55, 1))
        self.assertEqual(result['Make'], u'Canon')
        self.assertEqual(result['Model'], u'Canon EOS REBEL T3')
        self.assertEqual(result['LensModel'],
                         u'EF-S15-85mm f/3.5-5.6 IS USM')


class PhotoServiceTest(TestCase):

    def setUp(self):
        path = os.path.join(
            os.getcwd(),
            'photos/tests/fixtures/blake-small.jpg'
        )
        upload_file = open(path, 'rb')
        file = SimpleUploadedFile(upload_file.name, upload_file.read())
        self.maxDiff = None

        class Object(object):
            pass
        user = Object()
        user.username = 'Ryan'
        self.photo_service = PhotoService(file, user)

    def test_instance(self):
        self.assertIsInstance(self.photo_service, PhotoService)


class PhotoServiceUploadTest(TestCase):

    def setUp(self):
        pass

    def test_upload_photo(self):
        pass
