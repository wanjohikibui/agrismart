from django.conf.urls import patterns, include, url
from django.contrib import admin
from dss.views import * 
import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from dss.models import *
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views
from django.contrib.auth import urls
#from registration.backends.simple.views import *

admin.site.site_header = 'AgriDSS - The agriculture Revolution '

admin.autodiscover()
urlpatterns = patterns('',

			    url(r'^admin/', include(admin.site.urls)),
			    url(r'^markdown/', include("django_markdown.urls")),
			    url(r'^calendar/', include('django_bootstrap_calendar.urls')),
			    url(r'^', include('dss.urls')), 
			    url(r'^', include('cropper.urls')),
			    url(r'^', include('cal.urls')),  
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)

