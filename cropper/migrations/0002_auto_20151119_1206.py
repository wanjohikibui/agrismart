# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cropper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cropping',
            old_name='temperature_range',
            new_name='temperature',
        ),
        migrations.RemoveField(
            model_name='cropping',
            name='ph',
        ),
        migrations.AddField(
            model_name='cropping',
            name='ph',
            field=models.ManyToManyField(to='cropper.ph'),
        ),
        migrations.RemoveField(
            model_name='cropping',
            name='rainfall',
        ),
        migrations.AddField(
            model_name='cropping',
            name='rainfall',
            field=models.ManyToManyField(to='cropper.rainfall'),
        ),
        migrations.RemoveField(
            model_name='cropping',
            name='soil',
        ),
        migrations.AddField(
            model_name='cropping',
            name='soil',
            field=models.ManyToManyField(to='cropper.soil'),
        ),
    ]
