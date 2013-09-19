# Create your views here.
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from dashboard.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from resource.models import *
 
@login_required
def dashboard_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise,
    take them to the login page.
    """
    booking_list=Booked_resource.objects.filter(Booked_by=request.user.username)
    return render_to_response('portal/index.html',{'booking_list': booking_list},
                              context_instance=RequestContext(request))