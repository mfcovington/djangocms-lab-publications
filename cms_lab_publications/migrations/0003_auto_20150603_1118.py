# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_lab_publications', '0002_auto_20150527_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationset',
            name='bulk_pubmed_query',
            field=models.TextField(verbose_name='Bulk Query', help_text='Enter PubMed IDs and/or PubMed URLs to get or create multiple Publications and add them to this Publication Set.<br>PubMed IDs/URLs must be separated by commas or whitespace.<br>To add files and tags to publication records, create publications individually via the Publication Admin (or below).', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='redo_query',
            field=models.BooleanField(verbose_name='redo PubMed query?', default=False, help_text='Check this box to redo the PubMed query.<br>Any manual changes to the PubMed metadata will be overwritten.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='label',
            field=models.CharField(verbose_name='label', default='Publications', help_text='Enter a label for this Publication Set.<br>This will be the heading displayed above the publications.', max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='name',
            field=models.CharField(help_text="Enter a unique name for this Publication Set.<br>This won't be displayed on the site.", verbose_name='name', unique=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='pagination',
            field=models.PositiveIntegerField(verbose_name='pagination', default=0, help_text="How many publications should be displayed per page? To show all at once, enter '0'.<br>Server may need to be restarted for changes to take effect."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='publications',
            field=models.ManyToManyField(to='cms_lab_publications.Publication', null=True, blank=True),
            preserve_default=True,
        ),
    ]
