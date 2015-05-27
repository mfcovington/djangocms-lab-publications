# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('cms_lab_publications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicationset',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='publication',
            name='mini_citation',
            field=models.CharField(blank=True, max_length=255, help_text='<strong>This field is auto-generated when a PubMed query is made.</strong><br>It is recommended to use this text when adding custom names for uploaded files. See examples below.', verbose_name='mini citation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='cms_lab_publications_publication_image', help_text="Upload/select a representative image or figure for this publication.<br>Recommended naming format: '[mini citation] - Figure X'.", to='filer.Image', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='pdf',
            field=filer.fields.file.FilerFileField(related_name='cms_lab_publications_publication_pdf', help_text="Upload/select a PDF for this publication.<br>Recommended naming format: '[mini citation]'.", to='filer.File', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='supplemental_pdf',
            field=filer.fields.file.FilerFileField(related_name='cms_lab_publications_publication_supplemental_pdf', help_text="Upload/select a supplemental PDF for this publication.<br>Recommended naming format: '[mini citation] - Supplement'.", to='filer.File', blank=True, null=True),
            preserve_default=True,
        ),
    ]
