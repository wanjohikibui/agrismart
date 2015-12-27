from django.db import models
from django.contrib.gis.db import models
from django.core.urlresolvers import reverse

# Create your models here.
categories = (
	('Cereals','Cereals'),
	('Horticulture','Horticulture'),
	('Other','Other'),
)
rainrange = (
	('Less than 500mm','Less than 500mm'),
	('500mm - 1000mm','500mm - 1000mm'),
	('1000mm - 1500mm','1000mm - 1500mm'),
	('1500mm - 2500mm','1500mm - 2500mm'),
	('2500mm - 3500mm','2500mm - 3500mm'),
)

temperature=(
	('15 - 19','15 - 19'),
	('20 - 23','20 - 23'),
	('24 - 27','24 - 27'),
	('28 - 30','28 - 30'),
	('31 - 33','31 - 33'),
	('34 - 36','34 - 36'),
	)
class growthProperties(models.Model):
	code=models.IntegerField(primary_key=True)
	soil_type=models.CharField(max_length=100)
	rainfall = models.CharField(max_length=100, choices=rainrange)
	altitude= models.CharField(max_length=100)
	temperature_range = models.CharField(max_length=100, choices=temperature)

	def __unicode__(self):
		return "%s" %(self.code)

	class Meta:
		verbose_name_plural="Growth Properties"
		managed=True

class cropQuerySet(models.QuerySet):
	def approved(self):
		return self.filter(approved=True)


class landuse(models.Model):
	dn = models.IntegerField()
	area = models.FloatField()
	landuse = models.CharField(max_length=15)
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.landuse

	class Meta:
		verbose_name_plural = "Landuse"
		managed= True

class soil(models.Model):
	phaq = models.FloatField()
	drai_descr = models.CharField(max_length=32)
	slop = models.IntegerField()
	text = models.CharField(max_length=1)
	text_descr = models.CharField(max_length=18)
	rslo_descr = models.CharField(max_length=30)
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.text_descr

	class Meta:
		verbose_name_plural = "Soils"
		managed= True

class rainfall(models.Model):
	area = models.FloatField()
	perimeter = models.FloatField()
	rainfall_field = models.FloatField()
	rainfall_i = models.FloatField()
	type = models.CharField(max_length=10)
	color = models.IntegerField()
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.type

	class Meta:
		verbose_name_plural = "Rainfall"
		managed= True

class ph(models.Model):
	phaq = models.FloatField()
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.phaq)

	class Meta:
		verbose_name_plural = "Soil PH"
		managed= True


class temperature(models.Model):
	area = models.FloatField()
	perimeter = models.FloatField()
	temptra_field = models.FloatField()
	temptra_id = models.FloatField()
	tem = models.CharField(max_length=12)
	temrate = models.IntegerField()
	avg = models.IntegerField()
	geom = models.MultiPolygonField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.tem

	class Meta:
		verbose_name_plural = "Temperatures"
		managed= True
		
class elevation(models.Model):
	#id = models.IntegerField(primary_key=True)
	elev = models.FloatField()
	geom = models.MultiLineStringField(srid=4326)
	objects = models.GeoManager()

	def __unicode__(self):
		return unicode(self.elev)

	class Meta:
		verbose_name_plural = "Elevation Data"
		managed= True



class crop(models.Model):
	crop_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100, null=False)
	code = models.CharField(max_length=50, null=False)
	category = models.CharField(max_length=50, choices =categories, default=categories[0][0])
	seasons = models.CharField(max_length=100, null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True, null=True)
	description= models.TextField(null=True)
	#properties = models.ManyToManyField(growthProperties)
	soil =models.ManyToManyField(soil)
	rainfall = models.ManyToManyField(rainfall)
	elevation= models.ManyToManyField(elevation)
	temperature = models.ManyToManyField(temperature)
	ph = models.ManyToManyField(ph)
	approved = models.BooleanField(default=True)
	objects = cropQuerySet.as_manager()

	def __unicode__(self):
		return unicode(self.name)

	class Meta:
		verbose_name_plural = "Crops"
		managed= True

	def get_absolute_url(self):
		return reverse("crop_detail", kwargs={"slug": self.slug})

	def get_crops_count(self):
		return unicode(self.crop.count())

class cropping(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100, null=False)
	code = models.CharField(max_length=50, null=False)
	category = models.CharField(max_length=50, choices =categories, default=categories[0][0])
	seasons = models.CharField(max_length=100, null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True, null=True)
	soil =models.ManyToManyField(soil)
	rainfall = models.ManyToManyField(rainfall)
	altitude= models.ManyToManyField(elevation)
	temperature = models.ManyToManyField(temperature)
	ph = models.ManyToManyField(ph)
	description= models.TextField(null=True,blank=True)
	approved = models.BooleanField(default=False)
	objects = cropQuerySet.as_manager()

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Cropping Manager"
		managed= True

	def get_absolute_url(self):
		return reverse("crop_detail", kwargs={"slug": self.slug})

	def get_crops_count(self):
		return self.cropping.count()