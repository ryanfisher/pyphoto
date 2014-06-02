from django.test import TestCase

from photos.models import Photo
from profiles.models import User


class PhotosViewsNotLoggedInTests(TestCase):

    def test_edit(self):
        response = self.client.get('/manage')
        self.assertEquals(response.status_code, 302)


class PhotosViewsTests(TestCase):

    def setUp(self):
        User.objects.create(
            id=1,
            email='akopitar@lakings.com',
            profile_name='anze',
        )
        self.photo = Photo.objects.create(
            url="photos/photo.jpg",
            size=23423,
            user_id=1,
            height=800,
            width=1200,
            id=1
        )

    def tearDown(self):
        Photo.objects.all().delete()
        User.objects.all().delete()

    def test_show(self):
        response = self.client.get('/photos/1')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'bootstrapped_photo')

    def test_show_profile_url(self):
        response = self.client.get('/photos/1')
        self.assertContains(response, 'anze')

    def test_show_404(self):
        response = self.client.get('/photos/99')
        self.assertEquals(response.status_code, 404)


class PhotosIndexViewsTests(TestCase):

    def test_index(self):
        response = self.client.get('/photos')
        self.assertEquals(response.status_code, 302)
