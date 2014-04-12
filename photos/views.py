from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer

from photos.forms import PhotoUploadForm
from photos.models import Photo
from photos.services import PhotoService
from photos.serializers import PhotoSerializer


@login_required
def upload(request):
    if request.method != 'POST':
        raise Http404
    form = PhotoUploadForm(request.POST, request.FILES)
    if form.is_valid():
        request_file = request.FILES['file']
        try:
            # TODO Check for key in model before trying to upload
            service = PhotoService(request_file, request.user)
            photo = service.store_and_save_photos()
        except IntegrityError:
            return HttpResponse(status=409)
    serializer = PhotoSerializer(photo)
    return JSONResponse(serializer.data)


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


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its contents into JSON
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@login_required
def photo_list(request):
    """
    List all photos
    """
    if request.method == 'GET':
        photos = Photo.objects.filter(user=request.user)
        serializer = PhotoSerializer(photos, many=True)
        return JSONResponse(serializer.data)
    else:
        raise Http404

@csrf_exempt
@login_required
def photo_delete(request, id):
    Photo.objects.filter(user=request.user).get(id=id)
    if request.method == 'DELETE':
        return HttpResponse(status=200)
    else:
        raise Http404
