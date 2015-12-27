from django.conf.urls import patterns, include, url
from django.contrib import admin
from dss.views import * 
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
	url(r'^$', TemplateView.as_view(template_name='temp/index.html'), name='index'),
    url(r'^contacts/$','dss.views.contact', name='contacts'),
    url(r'^register/$', 'dss.views.register_user', name='register_user'),
    #url(r'^events/(?P&lt;event_id&gt;\d+)/export/', 'dss.views.export', name="event_ics_export"),
    url(r'^calendars/$', 'dss.views.calendar', name='calendar'),
    url(r'^feed/$', LatestPosts(), name="feed"),
    url(r'^index/', BlogIndex.as_view(), name="indexs"),
    url(r'^about/', 'dss.views.about', name="about"),
    url(r'^entry/(?P<slug>\S+)$', BlogDetail.as_view(), name="entry_detail"),
    url(r'^map/$', 'dss.views.map', name='map'),
    url(r'^incident/$', 'dss.views.incident_portal', name='incident'),
    url(r'^admin_data/$', GeoJSONLayerView.as_view(model=administration, properties=('id','kenya_id','kenya_field','location_b','females','males','total')), name='data'),
    url(r'^events_data/$', GeoJSONLayerView.as_view(model=Events, properties=('name','organizers','sponsors','date','location','venue','event_type')), name='events'),
    url(r'^incidence_data/$', GeoJSONLayerView.as_view(model=incidence, properties=('date_applied','incidence_id','status','incidence_title','category','county','closest_town')), name='incidencedata'),
    url(r'^points/$', 'dss.views.points', name='points'),
    url(r'^accounts/login/$', 'dss.views.user_login', name='login'),
    url(r'^accounts/logout/', 'dss.views.user_logout', name='loggedout'),                                                                                                                    
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register_success/', ('dss.views.register_success')),
    url(r'^apply/$', 'dss.views.application_portal', name='apply'),
    url(r'^status/$', 'dss.views.status', name='status'),
    url(r'^incidences/$', 'dss.views.add_point', name='incidences'),
    url(r'^add_point/error$', 'dss.views.form_error'),
    url(r'^add_point/success$', 'dss.views.form_success'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^confirm/(?P<activation_key>\w+)/', ('dss.views.register_confirm')),
    url(r'^password/$', 'django.contrib.auth.views.password_reset', {}, 'password_reset'),
    url(r'^accounts/password_change/$','django.contrib.auth.views.password_change', 
        {'post_change_redirect' : '/accounts/password_change/done/'}, 
        name="password_change"), 
    url(r'^accounts/password_change/done/$','django.contrib.auth.views.password_change_done'),
    url(r'^accounts/password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password_reset/mailed/'},
        name="password_reset"),
    url(r'^accounts/password_reset/mailed/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password_reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/accounts/password_reset/complete/'}),
    url(r'^accounts/password_reset/complete/$', 
        'django.contrib.auth.views.password_reset_complete') 
					    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
