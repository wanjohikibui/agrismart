from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from dss.models import *
from cropper.models import *
from django.contrib.gis import admin as geoadmin
from leaflet.admin import LeafletGeoAdmin
from django.db.models import signals
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField
#from django.contrib import databrowse

# Register your models here.
class StaffAdmin(UserAdmin):

    def queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
        return qs

class CustomerAdmin(StaffAdmin):

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.filter(Q(is_staff=False) | Q(is_superuser=False))
        return qs

class applicationAdmin (admin.ModelAdmin):
    list_display = ('app_id','user','first_name','last_name','email','telephone','date_applied','application_type','county','closest_town','status')
    search_fields = ['first_name','email'] 
    ordering = ['app_id']
    #readonly_fields = ['dc_comments ','upload_dcreport', 'final_comments']
    list_filter=('app_id','application_type')
    actions = ['send_EMAIL']

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


    def send_EMAIL(self, request, queryset):
        from django.core.mail import send_mail
        for i in queryset:
            if i.email:
                send_mail('Service Application', 'Hello,We aknowledge receipt of your application.It will be processed soon.', 'from@example.com',[i.email], fail_silently=False)
                message_bit = "Email sent successfully!!"
            else:
                self.message_user(request, "%s" % message_bit) 
    send_EMAIL.short_description = "Send an email to selected users"

def notify_admin(sender, instance, created, **kwargs):
    '''Notify the administrator that a new user has been added.'''
    if created:
       subject = 'New user created'
       message = 'User %s was added' % instance.username
       from_addr = 'no-reply@example.com'
       recipient_list = ('admin@example.com',)
       send_mail(subject, message, from_addr, recipient_list)

signals.post_save.connect(notify_admin, sender=User)

class incidenceAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('incidence_id','incidence_title','first_name','last_name','email','telephone','category','county','status','date_applied')
    search_fields = ['first_name','email'] 
    ordering = ['incidence_id']
    #readonly_fields = ['dc_comments ','upload_dcreport', 'final_comments']
    #filter_horizontal = ('authors',)
    list_filter=('incidence_id','category')
    default_lon =  4124488.98858#37.050093#
    default_lat =  -62466.02641  #-0.561360
    default_zoom = 14
    map_info = True
    map_width = 700
    map_height = 500

class eventsAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id','name','organizers','sponsors','venue','agenda','contacts','event_type','closest_town')
    search_fields = ['organizers','venue'] 
    ordering = ['id']
    #readonly_fields = ['dc_comments ','upload_dcreport', 'final_comments']
    list_filter=('id','date')
    default_lon =  4124488.98858#36.9654#
    default_lat =  -62466.02641  #-0.4030
    default_zoom = 14
    map_info = True
    map_width = 700
    map_height = 500

class administrationAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id','kenya_id','class1','class2','class3','class4','number','province_b','location_b','subloc_b','males','females','total','pop_km2','househds','av_hhs')
    search_fields = ['class4','location_b'] 
    ordering = ['kenya_id']
    #readonly_fields = ['dc_comments ','upload_dcreport', 'final_comments']
    list_filter=('class4','location_b')
    default_lon =  4124488.98858#36.9654#
    default_lat =  -62466.02641  #-0.4030
    default_zoom = 14
    map_info = True
    map_width = 700
    map_height = 500

class EntryAdmin(MarkdownModelAdmin):
    list_display = ("title", "created")
    prepopulated_fields = {"slug": ("title",)}
    # Next line is a workaround for Python 2.x
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    pass

class cropAdmin(MarkdownModelAdmin):
    list_display =('crop_id','name','code','category','seasons','approved')
    prepopulated_fields = {"slug": ("name",)}
    # Next line is a workaround for Python 2.x
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    pass

class croppingAdmin(MarkdownModelAdmin):
    def get_soil(self):
        return "\n " . join([x.__str__() for x in self.soil.all()])
    def get_rainfall(self):
        return "\n " . join([x.__str__() for x in self.rainfall.all()])
    def get_altitude(self):
        return "\n " . join([x.__str__() for x in self.altitude.all()])
    def get_temp(self):
        return "\n " . join([x.__str__() for x in self.temperature.all()])
    def get_ph(self):
        return "\n " . join([x.__str__() for x in self.ph.all()])


    list_display =('id','name','code','approved','category','seasons',get_soil,get_ph,get_temp,get_altitude,get_rainfall)
    get_soil.short_description = 'Soil'
    get_ph.short_description = 'Ph'
    get_temp.short_description = 'Temperature'
    get_altitude.short_description = 'Altitude'
    get_rainfall.short_description = 'Rainfall'
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name'] 
    ordering = ['id']
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    pass

class growthAdmin(admin.ModelAdmin):
    pass
    list_display =('code','soil_type','rainfall','altitude','temperature_range')
    

class tagAdmin(admin.ModelAdmin):
    pass

class landuseAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('dn','landuse')
    search_fields = ['landuse','dn'] 

class soilAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('drai_descr','slop','text','text_descr')
    search_fields = ['text_descr','text']

class rainfallAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('rainfall_field','rainfall_i','type','color')
    search_fields = ['type','rainfall_i']

class phAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id','phaq',)
    search_fields = ['phaq','id']

class temperatureAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('temptra_id','temptra_field','tem','temrate','avg')
    search_fields = ['tem','temrate']

class elevationAdmin (geoadmin.OSMGeoAdmin):
    list_display = ('id','elev')
    search_fields = ['id','elev']

admin.site.unregister(User)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(application, applicationAdmin)
admin.site.register(incidence, incidenceAdmin)
admin.site.register(Tag, tagAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Events, eventsAdmin)
admin.site.register(administration, administrationAdmin)
#admin.site.register(crop, cropAdmin)
admin.site.register(growthProperties, growthAdmin)
admin.site.register(landuse, landuseAdmin)
admin.site.register(soil, soilAdmin)
admin.site.register(rainfall, rainfallAdmin)
admin.site.register(ph, phAdmin)
admin.site.register(temperature, temperatureAdmin)
admin.site.register(elevation, elevationAdmin)
admin.site.register(cropping, croppingAdmin)
