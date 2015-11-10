# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_lab_publications', '0004_auto_20150624_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationset',
            name='publications',
            field=models.ManyToManyField(blank=True, to='cms_lab_publications.Publication'),
            preserve_default=True,
        ),
    ]
