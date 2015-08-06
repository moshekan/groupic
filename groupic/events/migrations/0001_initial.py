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
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('str_id', models.CharField(max_length=255)),
                ('is_public', models.BooleanField(default=False)),
                ('city', models.CharField(max_length=255)),
                ('bar_code', models.CharField(max_length=255)),
                ('admin', models.ForeignKey(related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(max_length=255)),
                ('full_res', models.CharField(max_length=255)),
                ('thumbnail', models.CharField(max_length=255)),
                ('event', models.ForeignKey(to='events.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
