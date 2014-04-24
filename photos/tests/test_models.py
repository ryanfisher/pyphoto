from django.test import TestCase

from photos.models import Photo


class PhotoTest(TestCase):
    def setUp(self):
        self.photo = Photo.objects.create(
            url='http://ryanfisher.io/image.jpg',
            optimized_url='http://ryanfisher.io/image.jpg',
            thumbnail_url='http://ryanfisher.io/image.jpg',
            original_filename='image.jpg',
            iso=400,
            width=1200,
            height=800,
            size=8000,
            user_id=1,
            camera_make='Canon',
            camera_model='Canon 7D',
            lens_model='Lens!',
            f_stop_denominator=1,
            f_stop_numerator=22,
            exposure_denominator=1,
            exposure_numerator=1,
            focal_length_denominator=1,
            focal_length_numerator=55
        )

    def test_instance(self):
        self.assertIsInstance(self.photo, Photo)
