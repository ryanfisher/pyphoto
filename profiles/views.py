from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def login_post(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/')

def login_view(request):
    if not request.GET:
        return render_to_response('profiles/login.html')
    elif request.POST:
        return login_post(request)
