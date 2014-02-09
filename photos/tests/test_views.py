from django.test import TestCase

from photos import views

class PhotosViewsTests(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_upload(self):
        response = self.client.get('/upload/')
        self.assertEquals(response.status_code, 200)
