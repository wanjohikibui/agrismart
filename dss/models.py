from django.db import models
from django.contrib.gis.db import models
import datetime 
from django.utils import timezone
from django.db.models import signals
from django.forms import TextInput
from django.contrib.auth.models import User,Group
from django.core.validators import MaxLengthValidator,MinLengthValidator
from django.template.defaultfilters import date
from django.core.urlresolvers import reverse
from phonenumber_field.modelfields import PhoneNumberField
#from django_hstore import hstore

def upload_application(instance, filename):
   # return "title_images/%s" % (filename)
    return '/'.join(['application_docs', str(instance.category), filename])

def upload_report(instance, filename):
    return "report_images/%s" % (filename)

def upload_docs(instance, filename):
    return "documents/%s" % (filename)

application_types=(
            ('Farm Inputs','Farm Inputs'),
            ('Farm  Inspection','Farm Inspection'),
            ('Agricultural Advice','Agricultural Advice'),
            ('Soil Testing','Soil Testing'),
            ('Other','Other'),
    )
category =(
            ('Pests','Pests'),
            ('Disease','Disease'),
            ('Natural Disaster ','Natural Disaster'),
            ('Other','Other'),
    )
locations = (
    ('Githii','Githii'),
    ('Muhito','Muhito'),
    ('Gakindu','Gakindu'),
    ('Gikondi','Gikondi'),

    )
status = (
    ('Unchecked','Unchecked'),
    ('Checked','Checked'),
    ('Approved','Approved'),
    ('Closed','Closed'),

    )

incidence_status = (
        ('Average','Average'),
        ('Bad','Bad'),
        ('Very Bad','Very Bad'),
        ('Unknown','Unknown'),

    )
event_type = (
        ('Seminar','Seminar'),
        ('Kamukunji','Kamukunji'),
        ('Road Show','Road Show'),
        ('Annual GM','Annual GM'),
        ('Other','Other'),
    )
# Create your models here.
class UserProfile(models.Model):
    
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today()) 
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural='User profiles'

class Customer(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Customer account'
        verbose_name_plural = 'Customer accounts'

class Staff(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Staff account'
        verbose_name_plural = 'Staff accounts'

class application(models.Model):
    user = models.OneToOneField(User, unique=False)
    app_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField(max_length=50, help_text='user@user.com')
    telephone = PhoneNumberField(null=True,blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    application_type = models.CharField(max_length=50, choices=application_types)
    county = models.CharField(max_length=50, choices=locations)
    Area_Name=models.CharField(max_length=15,null=True)
    closest_town=models.CharField(max_length=15,null=True)
    description = models.TextField(max_length=256)
    status = models.CharField(max_length=15, null=False, choices=status, default=status[0][0])
    
    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Applied Services" 
        managed = True
    
class Events(models.Model):
    """docstring for Events"""
    name= models.CharField(max_length=50, null=False)
    id= models.AutoField(primary_key=True)
    organizers= models.CharField(max_length=50, null=False)
    sponsors= models.CharField(max_length=50, null=False)
    #my_date = forms.DateField(initial=date.today(), widget=forms.DateInput(format = '%d.%m.%Y'), input_formats=('%d.%m.%Y',))
    date= models.DateField()
    location= models.CharField(max_length=50, null=False)
    venue= models.CharField(max_length=50, null=False)
    agenda= models.CharField(max_length=50, null=False)
    event_type= models.CharField(max_length=50, choices=event_type)
    description= models.TextField(max_length=250, null=False)
    closest_town= models.CharField(max_length=50, null=False)
    areaname= models.CharField(max_length=50, null=False)
    contacts= PhoneNumberField(blank=True)
    geom= models.PointField(srid=21037)
    objects=models.GeoManager()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Events" 
        managed = True
        


class incidence (models.Model):
    incidence_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    email = models.EmailField(max_length=50, help_text='user@user.com')
    telephone = PhoneNumberField(null=True,blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)
    incidence_title = models.CharField(max_length=50, help_text="e.g. Tomato Frost")
    category = models.CharField(max_length=50, choices=category) 
    county = models.CharField(max_length=50, choices=locations, default=locations[0][0])
    closest_town = models.CharField(max_length=50, null=True, help_text= 'Mweiga')
    #photo = models.ImageField(upload_to= upload_application, null=True, blank=True, help_text="Upload photo of incidence")
    photo = models.FileField(upload_to=upload_application, null=True, blank=True,)
    status = models.CharField(max_length=15, null=False, choices=incidence_status, default=incidence_status[0][0])
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.incidence_title

    @property
    def timeframe(self):
        return '%s - present' % date(self.date_applied, "n/j/Y")
    
    class Meta:
        verbose_name_plural = "Reported Incidences" 
        managed = True
 

class administration(models.Model):
    id = models.AutoField(primary_key=True)
    kenya_field = models.FloatField()
    kenya_id = models.FloatField()
    number = models.IntegerField()
    province_b = models.CharField(max_length=12)
    class1 = models.IntegerField()
    district_b = models.CharField(max_length=12)
    class2 = models.IntegerField()
    division_b = models.CharField(max_length=22)
    class3 = models.IntegerField()
    location_b = models.CharField(max_length=24)
    class4 = models.IntegerField()
    subloc_b = models.CharField(max_length=22)
    males = models.IntegerField()
    females = models.IntegerField()
    total = models.IntegerField()
    househds = models.IntegerField()
    pop_km2 = models.FloatField()
    hh_km2 = models.FloatField()
    av_hhs = models.FloatField()
    arekm2 = models.FloatField()
    dis = models.IntegerField()
    areakmsq = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):              # __unicode__ on Python 2
        return 'Type: %s' % self.location_b

    class Meta:
        verbose_name_plural = "Administration Sections" 
        managed = True


class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug


class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)


class Entry(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    objects = EntryQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "News Entry"
        verbose_name_plural = "News Entries"
        ordering = ["-created"]