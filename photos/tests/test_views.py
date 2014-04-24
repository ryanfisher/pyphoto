from django.test import TestCase

from photos.models import Photo


class PhotosViewsNotLoggedInTests(TestCase):

    def test_edit(self):
        response = self.client.get('/manage')
        self.assertEquals(response.status_code, 302)


class PhotosViewsTests(TestCase):

    def setUp(self):
        self.photo = Photo.objects.create(
            url="photos/photo.jpg",
            size=23423,
            user_id=1,
            height=800,
            width=1200,
            id=1
        )

    def test_show(self):
        response = self.client.get('/photos/1')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'photos/photo.jpg')

    def test_show_404(self):
        response = self.client.get('/photos/99')
        self.assertEquals(response.status_code, 404)


class PhotosIndexViewsTests(TestCase):

    def test_index(self):
        response = self.client.get('/photos')
        self.assertEquals(response.status_code, 302)
