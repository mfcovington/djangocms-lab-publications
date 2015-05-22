# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import filer.fields.file
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150514_0053'),
        ('cms', '0011_auto_20150419_1006'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pmid', models.IntegerField(blank=True, help_text="Enter publication's PubMed ID.", verbose_name='PubMed ID', unique=True)),
                ('pubmed_url', models.URLField(blank=True, help_text="Enter publication's PubMed URL.", verbose_name='PubMed URL', unique=True)),
                ('redo_query', models.BooleanField(help_text='Check this box to redo the PubMed query. Any manual changes to the PubMed metadata will be overwritten.', default=False, verbose_name='redo PubMed query?')),
                ('title', models.CharField(max_length=255, blank=True, verbose_name='title')),
                ('authors', models.TextField(blank=True, verbose_name='authors')),
                ('first_author', models.CharField(max_length=255, blank=True, verbose_name='first author')),
                ('last_author', models.CharField(max_length=255, blank=True, verbose_name='last author')),
                ('journal', models.CharField(max_length=255, blank=True, verbose_name='journal')),
                ('year', models.CharField(max_length=4, blank=True, verbose_name='year')),
                ('month', models.CharField(max_length=2, blank=True, verbose_name='month')),
                ('day', models.CharField(max_length=2, blank=True, verbose_name='day')),
                ('url', models.URLField(blank=True, verbose_name='publication URL')),
                ('citation', models.TextField(blank=True, verbose_name='citation')),
                ('abstract', models.TextField(blank=True, verbose_name='abstract')),
                ('image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True, related_name='cms_lab_publications_publication_image', help_text='Upload/select a representative image or figure for this publication.')),
                ('pdf', filer.fields.file.FilerFileField(blank=True, to='filer.File', null=True, related_name='cms_lab_publications_publication_pdf', help_text='Upload/select a PDF for this publication.')),
                ('supplemental_pdf', filer.fields.file.FilerFileField(blank=True, to='filer.File', null=True, related_name='cms_lab_publications_publication_supplemental_pdf', help_text='Upload/select a supplemental PDF for this publication.')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Tags')),
            ],
            options={
                'ordering': ('-year', '-month', '-day', 'first_author'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationSet',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, help_text="Enter a unique name for this Publication Set. This won't be displayed on the site.", verbose_name='name', unique=True)),
                ('label', models.CharField(max_length=255, help_text='Enter a label for this Publication Set. This may be displayed on the site.', verbose_name='label')),
                ('description', models.TextField(blank=True, help_text='Enter a description of this Publication Set.', verbose_name='description')),
                ('pagination', models.PositiveIntegerField(help_text="How many publications should be displayed per page? To show all at once, enter '0'. Server may need to be restarted for changes to take effect.", default=5, verbose_name='pagination')),
                ('searchable', models.BooleanField(help_text='Enable publication search and keyword filter.', default=True, verbose_name='searchable?')),
                ('publications', models.ManyToManyField(to='cms_lab_publications.Publication')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', through='taggit.TaggedItem', verbose_name='Tags')),
            ],
            options={
                'ordering': ('label',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationSetPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(to='cms.CMSPlugin', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('publication_set', models.ForeignKey(to='cms_lab_publications.PublicationSet')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
