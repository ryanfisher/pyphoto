from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from photos.forms import PhotoUploadForm
from photos.models import Photo, Album, SortedPhoto, Tag
from photos.services import PhotoService
from photos.serializers import PhotoSerializer, AlbumSerializer

import json


@login_required
def manage(request):
    photo_form = PhotoUploadForm()
    return render_to_response(
        'photos/manage.html',
        {'form': photo_form},
        context_instance=RequestContext(request)
    )


def index(request):
    photos = Photo.objects.all()[:40]
    serializer = PhotoSerializer(photos, many=True)
    photos = json.dumps(serializer.data)
    return render_to_response('photos/index.html', {'photos': photos})


@login_required
def edit(request):
    photos = Photo.objects.filter(user=request.user)
    serializer = PhotoSerializer(photos, many=True)
    photos = json.dumps(serializer.data)
    return render_to_response('photos/edit.html', {'photos': photos})


def show(request, id):
    photo = get_object_or_404(Photo, id=id)
    photo_data = PhotoSerializer(photo).data
    photo_hash = {
        'photo': photo,
        'display_url': photo.display_url(),
        'f_stop': photo.f_stop(),
        'shutter_speed': photo.shutter_speed(),
        'focal_length': photo.focal_length(),
        'public_tags': photo_data['public_tags'],
        'photo_data': json.dumps(photo_data),
    }
    return render_to_response(
        'photos/show.html',
        photo_hash,
        context_instance=RequestContext(request)
    )


def album_show(request, id):
    album = get_object_or_404(Album, id=id)
    serializer = AlbumSerializer(album)
    photos = json.dumps(serializer.data['photos'])
    return render_to_response(
        'photos/album_show.html',
        {'photos': photos, 'title': album.title}
    )


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

    def put(self, request, pk, format=None):
        photo = Photo.objects.get(id=pk, user=request.user)
        query = Q()
        for tag in request.DATA['public_tags']:
            query = query | Q(text=tag)
        photo.public_tags = Tag.objects.filter(query)
        photo.save()
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        photo = Photo.objects.filter(user=request.user).get(id=pk)
        photo.delete()
        return HttpResponse(status=200)


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
        # Remove photos from album that are not included in request
        photo_ids = [photo['id'] for photo in request.DATA['photos']]
        album.sortedphoto_set.exclude(photo__id__in=photo_ids).delete()
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

    def delete(self, request, pk, format=None):
        albums = Album.objects.filter(user=request.user)
        albums.get(id=pk).delete()
        return HttpResponse(status=204)
