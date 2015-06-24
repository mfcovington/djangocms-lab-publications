# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('cms_lab_publications', '0003_auto_20150603_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='no_query',
            field=models.BooleanField(default=False, verbose_name="Don't query PubMed", help_text="Check this box to prevent a PubMed query.<br>Instead, enter publication info manually in the section below labeled 'Auto-generated PubMed Metadata'.<br>This option is useful for when there is no PubMed record for the publication."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='pubmed_url',
            field=models.URLField(blank=True, verbose_name='PubMed URL', help_text="Enter publication's PubMed URL."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, verbose_name='Tags', help_text='Add keyword tags that represent this publication.', to='taggit.Tag', through='taggit.TaggedItem'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='pagination',
            field=models.PositiveIntegerField(verbose_name='pubs per page', default=0, help_text="How many publications should be displayed per page?<br>To show all at once, enter '0'."),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publicationset',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, verbose_name='Tags', help_text='Add keyword tags that represent this publication set.', to='taggit.Tag', through='taggit.TaggedItem'),
            preserve_default=True,
        ),
    ]
