from django.shortcuts import render_to_response

def upload(request):
    return render_to_response('photos/upload.html')
