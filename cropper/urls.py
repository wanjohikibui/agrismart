from django.conf.urls import patterns, include, url
from django.contrib import admin
from dss.feed import *
from cropper.views import * 
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import ListView
from dss.models import *
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView
from django.contrib.auth import views
from django.contrib.auth import urls


urlpatterns = patterns('',
    url(r'^crops/', cropIndex.as_view(), name="cropindex"),
    url(r'^crop/(?P<slug>\S+)$', cropDetail.as_view(), name="crop_detail"),
    url(r'^landuse_data/$', GeoJSONLayerView.as_view(model=landuse, properties=('dn','landuse')), name='landuse'),
    url(r'^soil_data/$', GeoJSONLayerView.as_view(model=soil, properties=('drai_descr','slop','text','text_descr')), name='soil'),
    url(r'^ph_data/$', GeoJSONLayerView.as_view(model=ph, properties=('id','phaq',)), name='ph'),
    url(r'^temperature_data/$', GeoJSONLayerView.as_view(model=temperature, properties=('temptra_id','temptra_field','tem','temrate','avg')), name='temperature'),
    url(r'^rainfall_data/$', GeoJSONLayerView.as_view(model=rainfall, properties=('rainfall_field','rainfall_i','type','color')), name='rainfall'),
    url(r'^elevation_data/$', GeoJSONLayerView.as_view(model=elevation, properties=('id','elev')), name='contours'),
    url(r'^planner/$', 'cropper.views.planner', name='planner'),  
    url(r'^analyzer/$', 'cropper.views.analyzer', name='analyzer'),  
					    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
