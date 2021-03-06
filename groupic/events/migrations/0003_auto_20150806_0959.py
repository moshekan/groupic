# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150806_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(default=None, related_name='user', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
