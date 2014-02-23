from django.test import TestCase

from photos import views
from photos.models import Photo

class PhotosViewsNotLoggedInTests(TestCase):

    def test_upload(self):
        response = self.client.get('/upload')
        self.assertEquals(response.status_code, 302)

class PhotosViewsTests(TestCase):

    def test_show(self):
        response = self.client.get('photos/99')
        self.assertEquals(response.status_code, 404)
