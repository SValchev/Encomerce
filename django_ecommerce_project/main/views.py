# Create your views here.
from django.shortcuts import render_to_response, RequestContext
from .models import Status

from payments.models import User

def index(request):
    uid = request.session.get('user')
    if uid is None:
        return render_to_response('main/index.html')
    else:
        status = Status.objects.all().filter().order_by('-time_added')[:20]

        return render_to_response(
                                  'main/user.html',
                                  {'user':User.get_user_by_id(uid), 'report':status},
                                   context_instance=RequestContext(request))

def report_status(request):
    if request.method == 'POST':
        status = request.POST.get("status", "")
        if status:
            uid = request.session.get('user')
            user = User.get_user_by_id(uid)
            Status(user=user, status=status).save()

        return index(request)
