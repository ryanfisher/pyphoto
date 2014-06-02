import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from photos.services import PhotoService, ExifInfo, TemporaryImageFile


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

    def test_make(self):
        self.assertEqual(self.exif_info.make(), u'Canon')

    def test_f_stop_numerator(self):
        self.assertEqual(self.exif_info.f_stop_numerator(), 5)

    def test_f_stop_denominator(self):
        self.assertEqual(self.exif_info.f_stop_denominator(), 1)

    def test_exposure_numerator(self):
        self.assertEqual(self.exif_info.exposure_numerator(), 1)

    def test_exposure_denominator(self):
        self.assertEqual(self.exif_info.exposure_denominator(), 100)

    def test_iso(self):
        self.assertEqual(self.exif_info.iso(), 800)

    def test_focal_length_numerator(self):
        self.assertEqual(self.exif_info.focal_length_numerator(), 55)

    def test_focal_length_denominator(self):
        self.assertEqual(self.exif_info.focal_length_denominator(), 1)

    def test_lens_model(self):
        self.assertEqual(self.exif_info.lens_model(),
                         u'EF-S15-85mm f/3.5-5.6 IS USM')

    def test_exif(self):
        result = self.exif_info.get_dictionary()
        self.assertEqual(result['ISOSpeedRatings'], 800)


class ExifInfoNoneTest(TestCase):

    def setUp(self):
        path = os.path.join(
            os.getcwd(),
            'photos/tests/fixtures/cheesesteak.jpg'
        )
        img = Image.open(path)
        self.exif_info = ExifInfo(img)

    def test_model(self):
        self.assertEqual(self.exif_info.model(), None)

    def test_make(self):
        self.assertEqual(self.exif_info.make(), None)

    def test_f_stop_numerator(self):
        self.assertEqual(self.exif_info.f_stop_numerator(), None)

    def test_f_stop_denominator(self):
        self.assertEqual(self.exif_info.f_stop_denominator(), None)

    def test_exposure_numerator(self):
        self.assertEqual(self.exif_info.exposure_numerator(), None)

    def test_exposure_denominator(self):
        self.assertEqual(self.exif_info.exposure_denominator(), None)

    def test_iso(self):
        self.assertEqual(self.exif_info.iso(), None)

    def test_focal_length_numerator(self):
        self.assertEqual(self.exif_info.focal_length_numerator(), None)

    def test_focal_length_denominator(self):
        self.assertEqual(self.exif_info.focal_length_denominator(), None)

    def test_lens_model(self):
        self.assertEqual(self.exif_info.lens_model(), None)


class TemporaryImageFileTest(TestCase):

    def setUp(self):
        path = os.path.join(
            os.getcwd(),
            'photos/tests/fixtures/blake-small.jpg'
        )
        upload_file = open(path, 'rb')
        file = SimpleUploadedFile(upload_file.name, upload_file.read())
        self.tmp_file = TemporaryImageFile(file)

    def tearDown(self):
        self.tmp_file.delete()

    def test_instance(self):
        self.assertIsInstance(self.tmp_file, TemporaryImageFile)


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
        user.profile_name = 'Ryan'
        self.photo_service = PhotoService(file, user)

    def test_instance(self):
        self.assertIsInstance(self.photo_service, PhotoService)


class PhotoServiceUploadTest(TestCase):

    def setUp(self):
        pass

    def test_upload_photo(self):
        pass
