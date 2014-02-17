from django.test import TestCase

from photos import views

class PhotosViewsNotLoggedInTests(TestCase):

    def test_upload(self):
        response = self.client.get('/upload/')
        self.assertEquals(response.status_code, 302)
