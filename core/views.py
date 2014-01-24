from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def root(request):
    return render_to_response('core/index.html')
