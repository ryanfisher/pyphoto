from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from photos.forms import PhotoUploadForm
from photos.models import Photo, Album, SortedPhoto
from photos.services import PhotoService
from photos.serializers import PhotoSerializer, AlbumSerializer


@login_required
def manage(request):
    photo_form = PhotoUploadForm()
    return render_to_response(
        'photos/manage.html',
        {'form': photo_form},
        context_instance=RequestContext(request)
    )


@login_required
def index(request):
    photos = Photo.objects.filter(user=request.user)
    return render_to_response('photos/index.html', {'photos': photos})


@login_required
def edit(request):
    photos = Photo.objects.filter(user=request.user)
    return render_to_response('photos/edit.html', {'photos': photos})


def show(request, id):
    photo = get_object_or_404(Photo, id=id)
    photo_hash = {
        'photo': photo,
        'display_url': photo.display_url(),
        'f_stop': photo.f_stop(),
        'shutter_speed': photo.shutter_speed(),
        'focal_length': photo.focal_length(),
    }
    return render_to_response('photos/show.html', photo_hash)


def album_show(request, id):
    album = get_object_or_404(Album, id=id)
    serializer = AlbumSerializer(album)
    return render_to_response('photos/album_show.html', serializer.data)


# TODO Make sure login is required for these methods
class PhotoList(APIView):
    def get(self, request, format=None):
        """
        List all photos
        """
        photos = Photo.objects.filter(user=request.user)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request_file = request.FILES['file']
            try:
                service = PhotoService(request_file, request.user)
                if service.photo_exists():
                    raise IntegrityError
                photo = service.store_and_save_photos()
            except IntegrityError:
                return HttpResponse(status=409)
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)


class AlbumList(APIView):
    def get(self, request, format=None):
        """
        List all albums
        """
        albums = Album.objects.filter(user=request.user)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # TODO Handle errors, use rest_framework
        album = Album.objects.create(
            user=request.user,
            title=request.DATA['title']
        )
        serializer = AlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        album = get_object_or_404(Album, id=pk)
        position = album.photos.count() + 1
        for photo in request.DATA['photos']:
            try:
                sorted_photo = album.sortedphoto_set.get(
                    photo__id=photo['id'],
                    photo__user=request.user
                )
                if 'position' in photo:
                    sorted_photo.position = photo['position']
                    sorted_photo.save()
            except SortedPhoto.DoesNotExist:
                SortedPhoto.objects.create(
                    album=album,
                    photo=Photo.objects.get(user=request.user, id=photo['id']),
                    position=position
                )
                position += 1
        serializer = AlbumSerializer(Album.objects.get(id=pk))
        return Response(serializer.data)


@login_required
def photo_delete(request, id):
    if request.method != 'DELETE':
        raise Http404
    photo = Photo.objects.filter(user=request.user).get(id=id)
    photo.delete()
    return HttpResponse(status=200)
