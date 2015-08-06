# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150806_1001'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='bar_code',
            new_name='barcode',
        ),
        migrations.RemoveField(
            model_name='media',
            name='url',
        ),
    ]
