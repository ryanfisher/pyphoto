from django.test import TestCase

from photos.services import PhotoService

class PhotoServiceTest(TestCase):

    def setUp(self):
        self.photo_service = PhotoService()

    def test_instance(self):
        self.assertIsInstance(self.photo_service, PhotoService)
