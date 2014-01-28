from django.shortcuts import redirect, render_to_response
from django.conf import settings
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from photos import forms


@login_required
def upload(request):
    if request.method == 'GET':
        image_form = forms.ImageUploadForm()
        return render_to_response(
            'photos/upload.html',
            {'form': image_form},
            context_instance=RequestContext(request)
        )
    elif request.method == 'POST':
        forms.ImageUploadForm(request.POST)
        return redirect('/')
