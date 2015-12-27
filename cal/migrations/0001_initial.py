# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entryy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('snippet', models.CharField(max_length=150, blank=True)),
                ('body', models.TextField(max_length=10000, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(blank=True)),
                ('remind', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
    ]
