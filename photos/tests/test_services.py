from django.test import TestCase

from photos.services import PhotoService

import os

class PhotoServiceTest(TestCase):

    def setUp(self):
        path = os.path.join(os.getcwd(), 'photos/tests/fixtures/blake-small.jpg')
        self.maxDiff = None
        self.photo_service = PhotoService(path)

    def test_instance(self):
        self.assertIsInstance(self.photo_service, PhotoService)

    def test_get_exif(self):
        result = self.photo_service.get_exif()
        self.assertEqual(result['ExposureTime'], (1, 100))
        self.assertEqual(result['FNumber'], (5, 1))
        self.assertEqual(result['ISOSpeedRatings'], 800)
        self.assertEqual(result['FocalLength'], (55, 1))
        self.assertEqual(result['Make'], u'Canon')
        self.assertEqual(result['Model'], u'Canon EOS REBEL T3')
        self.assertEqual(result['LensModel'], u'EF-S15-85mm f/3.5-5.6 IS USM')
