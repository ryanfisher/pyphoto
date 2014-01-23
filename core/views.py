from django.shortcuts import redirect, render_to_response

def root(request):
    if request.user.is_authenticated():
        return render_to_response('core/index.html')
    else:
        return redirect('/login')
