# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='crop',
            fields=[
                ('crop_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('category', models.CharField(default=b'Cereals', max_length=50, choices=[(b'Cereals', b'Cereals'), (b'Horticulture', b'Horticulture'), (b'Other', b'Other')])),
                ('seasons', models.CharField(max_length=100, null=True, blank=True)),
                ('slug', models.SlugField(max_length=200, unique=True, null=True)),
                ('description', models.TextField(null=True)),
                ('approved', models.BooleanField(default=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Crops',
            },
        ),
        migrations.CreateModel(
            name='cropping',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('category', models.CharField(default=b'Cereals', max_length=50, choices=[(b'Cereals', b'Cereals'), (b'Horticulture', b'Horticulture'), (b'Other', b'Other')])),
                ('seasons', models.CharField(max_length=100, null=True, blank=True)),
                ('slug', models.SlugField(max_length=200, unique=True, null=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('approved', models.BooleanField(default=True)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Cropping Manager',
            },
        ),
        migrations.CreateModel(
            name='elevation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elev', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='growthProperties',
            fields=[
                ('code', models.IntegerField(serialize=False, primary_key=True)),
                ('soil_type', models.CharField(max_length=100)),
                ('rainfall', models.CharField(max_length=100, choices=[(b'Less than 500mm', b'Less than 500mm'), (b'500mm - 1000mm', b'500mm - 1000mm'), (b'1000mm - 1500mm', b'1000mm - 1500mm'), (b'1500mm - 2500mm', b'1500mm - 2500mm'), (b'2500mm - 3500mm', b'2500mm - 3500mm')])),
                ('altitude', models.CharField(max_length=100)),
                ('temperature_range', models.CharField(max_length=100, choices=[(b'15 - 19', b'15 - 19'), (b'20 - 23', b'20 - 23'), (b'24 - 27', b'24 - 27'), (b'28 - 30', b'28 - 30'), (b'31 - 33', b'31 - 33'), (b'34 - 36', b'34 - 36')])),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Growth Properties',
            },
        ),
        migrations.CreateModel(
            name='landuse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dn', models.IntegerField()),
                ('area', models.FloatField()),
                ('landuse', models.CharField(max_length=15)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Landuse',
            },
        ),
        migrations.CreateModel(
            name='ph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phaq', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Soil PH',
            },
        ),
        migrations.CreateModel(
            name='rainfall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.FloatField()),
                ('perimeter', models.FloatField()),
                ('rainfall_field', models.FloatField()),
                ('rainfall_i', models.FloatField()),
                ('type', models.CharField(max_length=10)),
                ('color', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Rainfall',
            },
        ),
        migrations.CreateModel(
            name='soil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phaq', models.FloatField()),
                ('drai_descr', models.CharField(max_length=32)),
                ('slop', models.IntegerField()),
                ('text', models.CharField(max_length=1)),
                ('text_descr', models.CharField(max_length=18)),
                ('rslo_descr', models.CharField(max_length=30)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Soils',
            },
        ),
        migrations.CreateModel(
            name='temperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.FloatField()),
                ('perimeter', models.FloatField()),
                ('temptra_field', models.FloatField()),
                ('temptra_id', models.FloatField()),
                ('tem', models.CharField(max_length=12)),
                ('temrate', models.IntegerField()),
                ('avg', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'Temperatures',
            },
        ),
        migrations.AddField(
            model_name='cropping',
            name='altitude',
            field=models.ManyToManyField(to='cropper.elevation'),
        ),
        migrations.AddField(
            model_name='cropping',
            name='ph',
            field=models.ForeignKey(to='cropper.ph'),
        ),
        migrations.AddField(
            model_name='cropping',
            name='rainfall',
            field=models.ForeignKey(to='cropper.rainfall'),
        ),
        migrations.AddField(
            model_name='cropping',
            name='soil',
            field=models.ForeignKey(to='cropper.soil'),
        ),
        migrations.AddField(
            model_name='cropping',
            name='temperature_range',
            field=models.ManyToManyField(to='cropper.temperature'),
        ),
        migrations.AddField(
            model_name='crop',
            name='elevation',
            field=models.ManyToManyField(to='cropper.elevation'),
        ),
        migrations.AddField(
            model_name='crop',
            name='ph',
            field=models.ManyToManyField(to='cropper.ph'),
        ),
        migrations.AddField(
            model_name='crop',
            name='rainfall',
            field=models.ManyToManyField(to='cropper.rainfall'),
        ),
        migrations.AddField(
            model_name='crop',
            name='soil',
            field=models.ManyToManyField(to='cropper.soil'),
        ),
        migrations.AddField(
            model_name='crop',
            name='temperature',
            field=models.ManyToManyField(to='cropper.temperature'),
        ),
    ]
