from django.test import TestCase

from photos import services

class ImageServiceTest(TestCase):

    def setUp(self):
        self.image_service = services.ImageService()

    def test_instance(self):
        self.assertIsInstance(self.image_service, services.ImageService)
