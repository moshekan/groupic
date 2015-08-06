# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20150806_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='full_res',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='media',
            name='thumbnail',
            field=models.TextField(),
        ),
    ]
