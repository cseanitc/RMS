from django.conf.urls import patterns, include, url
from rms.views import *
from django.conf.urls.defaults import *
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import patterns, include
from dajaxice.core import dajaxice_autodiscover, dajaxice_config 
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

dajaxice_autodiscover()
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


# These urls are mapping to different views in views.py file.
urlpatterns = patterns('',
	 # Home page of RMS
	(r'^$', main_page),
	
	 # Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
	
    (r'^logout/$', logout_page),
	
	# Serve static content. This line is important to serve the static content i.e the css,javascript files.
	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
    
	# User profile page
	(r'^profile/$', profile),
	
	#Booking page
    (r'^booking/$', booking),
    (r'^changepass/$', 'django.contrib.auth.views.password_change'), 
    (r'^done/$', 'django.contrib.auth.views.password_change_done'),
    #Guest user page
    (r'^guest/$', guest),
	
	# User homepage.
    (r'^dashboard/', include('dashboard.urls')),
	
	# New user registration page
    (r'^registration/$',register),
	
	
	# FAQs page
    (r'^help/$',help),

    # Creditss page
    (r'^credits/$',credits),
	
	#This mapping is important for incorporating Django's Admin module in our project. If removed Admin module won't work.
    (r'^admin/', include(admin.site.urls)),
	
	# This line imports Dajaxice settings in our project, Important for AJAX functionality in our project. If removed AJAX functionality won't work.
    #oldstyle
    #(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    #newstyle
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
		
)

urlpatterns += staticfiles_urlpatterns()