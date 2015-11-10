import re

from django.db import models
from django.core.exceptions import ValidationError

from cms.models import CMSPlugin
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from taggit.managers import TaggableManager
import pubmed_lookup


class Publication(models.Model):

    pmid = models.IntegerField('PubMed ID',
        blank=True,
        help_text="Enter publication's PubMed ID.",
        unique=True,
    )
    pubmed_url = models.URLField('PubMed URL',
        blank=True,
        help_text="Enter publication's PubMed URL.",
    )
    redo_query = models.BooleanField('redo PubMed query?',
        default=False,
        help_text='Check this box to redo the PubMed query.<br>Any manual '
                  'changes to the PubMed metadata will be overwritten.',
    )
    no_query = models.BooleanField("Don't query PubMed",
        default=False,
        help_text="Check this box to prevent a PubMed query.<br>"
                  "Instead, enter publication info manually in the section below labeled "
                  "'Auto-generated PubMed Metadata'.<br>"
                  "This option is useful for when there is no PubMed record for the publication.",
    )

    pdf = FilerFileField(
        blank=True,
        null=True,
        help_text="Upload/select a PDF for this publication.<br>"
                  "Recommended naming format: '[mini citation]'.",
        related_name='%(app_label)s_%(class)s_pdf',
    )
    supplemental_pdf = FilerFileField(
        blank=True,
        null=True,
        help_text="Upload/select a supplemental PDF for this publication.<br>"
                  "Recommended naming format: '[mini citation] - Supplement'.",
        related_name='%(app_label)s_%(class)s_supplemental_pdf',
    )

    image = FilerImageField(
        blank=True,
        null=True,
        help_text="Upload/select a representative image or figure "
                  "for this publication.<br>"
                  "Recommended naming format: '[mini citation] - Figure X'.",
        related_name='%(app_label)s_%(class)s_image',
    )

    tags = TaggableManager(
        help_text='Add keyword tags that represent this publication.',
        blank=True,
    )

    title = models.CharField('title',
        blank=True,
        max_length=255,
    )
    authors = models.TextField('authors',
        blank=True,
    )
    first_author = models.CharField('first author',
        blank=True,
        max_length=255,
    )
    last_author = models.CharField('last author',
        blank=True,
        max_length=255,
    )
    journal = models.CharField('journal',
        blank=True,
        max_length=255,
    )
    year = models.CharField('year',
        blank=True,
        max_length=4,
    )
    month = models.CharField('month',
        blank=True,
        max_length=2,
    )
    day = models.CharField('day',
        blank=True,
        max_length=2,
    )
    url = models.URLField('publication URL',
        blank=True,
    )
    citation = models.TextField('citation',
        blank=True,
    )
    mini_citation = models.CharField('mini citation',
        blank=True,
        help_text='<strong>This field is auto-generated when a PubMed query '
                  'is made.</strong><br>'
                  'It is recommended to use this text when adding custom '
                  'names for uploaded files. See examples below.',
        max_length=255,
    )
    abstract = models.TextField('abstract',
        blank=True,
    )

    def clean(self):
        if not self.pk:
            if self.pmid and self.pubmed_url:
                raise ValidationError(
                    "Enter a PubMed ID or a PubMed URL, but not both.")

            if self.pmid == "" and self.pubmed_url == "":
                raise ValidationError("Enter a PubMed ID or a PubMed URL.")

    def save(self, *args, **kwargs):
        """
        Before saving, get publication's PubMed metadata if publication
        is not already in database or if 'redo_query' is True.
        """
        if self.no_query:
            if not self.pk or self.pmid > 0:
                try:
                    pmid_min = Publication.objects.all().aggregate(
                        models.Min('pmid'))['pmid__min'] - 1
                except:
                    self.pmid = 0
                else:
                    self.pmid = min(0, pmid_min)

            self.pubmed_url = ''
            self.mini_citation = '{} - {} - {}'.format(
                self.first_author, self.year, self.journal)

        elif self.redo_query or not self.pk:
            if self.pmid:
                query = self.pmid
            else:
                query = self.pubmed_url

            email = ""    # FIX THIS: Use logged-in user's email
            lookup = pubmed_lookup.PubMedLookup(query, email)
            publication = pubmed_lookup.Publication(lookup)

            self.pmid = publication.pmid
            self.pubmed_url = publication.pubmed_url

            self.title = publication.title
            self.authors = publication.authors
            self.first_author = publication.first_author
            self.last_author = publication.last_author
            self.journal = publication.journal
            self.year = publication.year
            self.month = publication.month
            self.day = publication.day
            self.url = publication.url
            self.citation = publication.cite()
            self.mini_citation = publication.cite_mini()
            self.abstract = publication.abstract

        self.redo_query = False

        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {} - {} - {} [{}]".format(self.year,
            self.first_author, self.journal, self.title, str(self.pmid),)

    class Meta:
        ordering = ('-year', '-month', '-day', 'first_author')


class PublicationSet(models.Model):

    name = models.CharField('name',
        help_text="Enter a unique name for this Publication Set.<br>"
                  "This won't be displayed on the site.",
        max_length=255,
        unique=True,
    )
    label = models.CharField('label',
        default='Publications',
        help_text='Enter a label for this Publication Set.<br>'
                  'This will be the heading displayed above the publications.',
        max_length=255,
    )
    description = models.TextField('description',
        blank=True,
        help_text='Enter a description of this Publication Set.',
    )

    pagination = models.PositiveIntegerField('pubs per page',
        default=0,
        help_text="How many publications should be displayed per page?<br>"
                  "To show all at once, enter '0'.",
    )

    bulk_pubmed_query = models.TextField('Bulk Query',
        blank=True,
        help_text='Enter PubMed IDs and/or PubMed URLs to get or create '
                  'multiple Publications and add them to this Publication Set.<br>'
                  'PubMed IDs/URLs must be separated by commas or whitespace.<br>'
                  'To add files and tags to publication records, create publications '
                  'individually via the Publication Admin (or below).',
    )
    publications = models.ManyToManyField(Publication,
        blank=True,
    )

    searchable = models.BooleanField('searchable?',
        default=True,
        help_text='Enable publication search and keyword filter.',
    )

    tags = TaggableManager(
        help_text='Add keyword tags that represent this publication set.',
        blank=True,
    )

    def perform_bulk_pubmed_query(self):
        """
        If 'bulk_pubmed_query' contains any content, perform a bulk PubMed query,
        add the publications to the publication set, and save.
        """
        if self.bulk_pubmed_query:
            failed_queries = []
            pmid_list = re.findall(r'(\d+)(?:[\s,]+|$)', self.bulk_pubmed_query)

            for pmid in pmid_list:
                try:
                    p, created = Publication.objects.get_or_create(pmid=pmid)
                except:
                    failed_queries.append(pmid)
                else:
                    self.publications.add(p.id)

            if failed_queries:
                failed_queries.sort(key=int)
                self.bulk_pubmed_query = 'FAILED QUERIES: {}'.format(', '.join(failed_queries))
            else:
                self.bulk_pubmed_query = ''

    def clean(self):
        """
        Require creation of Publication Set before performing a Bulk PubMed Query.
        """
        if self.bulk_pubmed_query and self.pk is None:
            raise ValidationError(
                'Can only perform a Bulk PubMed Query with an existing Publication Set. '
                'First create this Publication Set and then do the Bulk PubMed Query.'
            )

    def save(self, *args, **kwargs):
        """
        Before saving, execute 'perform_bulk_pubmed_query()'.
        """
        self.perform_bulk_pubmed_query()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class PublicationSetPlugin(CMSPlugin):
    publication_set = models.ForeignKey('cms_lab_publications.PublicationSet')

    def __str__(self):
        return self.publication_set.name
