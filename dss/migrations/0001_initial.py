# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.gis.db.models.fields
from django.conf import settings
import dss.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='administration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('kenya_field', models.FloatField()),
                ('kenya_id', models.FloatField()),
                ('number', models.IntegerField()),
                ('province_b', models.CharField(max_length=12)),
                ('class1', models.IntegerField()),
                ('district_b', models.CharField(max_length=12)),
                ('class2', models.IntegerField()),
                ('division_b', models.CharField(max_length=22)),
                ('class3', models.IntegerField()),
                ('location_b', models.CharField(max_length=24)),
                ('class4', models.IntegerField()),
                ('subloc_b', models.CharField(max_length=22)),
                ('males', models.IntegerField()),
                ('females', models.IntegerField()),
                ('total', models.IntegerField()),
                ('househds', models.IntegerField()),
                ('pop_km2', models.FloatField()),
                ('hh_km2', models.FloatField()),
                ('av_hhs', models.FloatField()),
                ('arekm2', models.FloatField()),
                ('dis', models.IntegerField()),
                ('areakmsq', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Administration Sections',
            },
        ),
        migrations.CreateModel(
            name='application',
            fields=[
                ('app_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(help_text=b'user@user.com', max_length=50)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('application_type', models.CharField(max_length=50, choices=[(b'Farm Inputs', b'Farm Inputs'), (b'Farm  Inspection', b'Farm Inspection'), (b'Agricultural Advice', b'Agricultural Advice'), (b'Soil Testing', b'Soil Testing'), (b'Other', b'Other')])),
                ('county', models.CharField(max_length=50, choices=[(b'Githii', b'Githii'), (b'Kirinyaga', b'Kirinyaga'), (b'Kiambu', b'Kiambu'), (b'Laikipia', b'Laikipia')])),
                ('Area_Name', models.CharField(max_length=15, null=True)),
                ('closest_town', models.CharField(max_length=15, null=True)),
                ('description', models.TextField(max_length=256)),
                ('status', models.CharField(default=b'Unchecked', max_length=15, choices=[(b'Unchecked', b'Unchecked'), (b'Checked', b'Checked'), (b'Approved', b'Approved'), (b'Closed', b'Closed')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Applied Services',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'News Entry',
                'verbose_name_plural': 'News Entries',
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('organizers', models.CharField(max_length=50)),
                ('sponsors', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=50)),
                ('venue', models.CharField(max_length=50)),
                ('agenda', models.CharField(max_length=50)),
                ('event_type', models.CharField(max_length=50, choices=[(b'Seminar', b'Seminar'), (b'Kamukunji', b'Kamukunji'), (b'Road Show', b'Road Show'), (b'Annual GM', b'Annual GM')])),
                ('description', models.TextField(max_length=250)),
                ('closest_town', models.CharField(max_length=50)),
                ('areaname', models.CharField(max_length=50)),
                ('contacts', phonenumber_field.modelfields.PhoneNumberField(max_length=128, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=21037)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='incidence',
            fields=[
                ('incidence_id', models.AutoField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(help_text=b'user@user.com', max_length=50)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('incidence_title', models.CharField(help_text=b'e.g. Tomato Frost', max_length=50)),
                ('category', models.CharField(max_length=50, choices=[(b'Pests', b'Pests'), (b'Disease', b'Disease'), (b'Natural Disaster ', b'Natural Disaster'), (b'Other', b'Other')])),
                ('county', models.CharField(max_length=50, choices=[(b'Githii', b'Githii'), (b'Kirinyaga', b'Kirinyaga'), (b'Kiambu', b'Kiambu'), (b'Laikipia', b'Laikipia')])),
                ('closest_town', models.CharField(help_text=b'Mweiga', max_length=50, null=True)),
                ('photo', models.FileField(null=True, upload_to=dss.models.upload_application, blank=True)),
                ('status', models.CharField(default=b'Average', max_length=15, choices=[(b'Average', b'Average'), (b'Bad', b'Bad'), (b'Very Bad', b'Very Bad'), (b'Unknown', b'Unknown')])),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Reported Incidences',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.date(2015, 11, 19))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='dss.Tag'),
        ),
    ]
