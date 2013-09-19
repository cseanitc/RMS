from django.conf.urls.defaults import *
from dashboard.views import *
 
urlpatterns = patterns('',
 
    # Main web portal entrance.
    (r'^$', dashboard_main_page),
 
)