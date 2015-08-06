# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='admin',
            field=models.ForeignKey(related_name='admin', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(default=None, related_name='user', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
