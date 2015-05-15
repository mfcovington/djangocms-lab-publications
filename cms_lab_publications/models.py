from django.db import models
from django.core.exceptions import ValidationError

from cms.models import CMSPlugin
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
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
        unique=True,
    )
    redo_query = models.BooleanField('redo PubMed query?',
        default=False,
        help_text='Check this box to redo the PubMed query. Any manual ' \
                  'changes to the PubMed metadata will be overwritten.',
    )

    pdf = FilerFileField(
        blank=True,
        null=True,
        help_text='Upload/select a PDF for this publication.',
        related_name='%(app_label)s_%(class)s_pdf',
    )
    supplemental_pdf = FilerFileField(
        blank=True,
        null=True,
        help_text='Upload/select a supplemental PDF for this publication.',
        related_name='%(app_label)s_%(class)s_supplemental_pdf',
    )

    image = FilerImageField(
        blank=True,
        null=True,
        help_text='Upload/select a representative image or figure ' \
                  'for this publication.',
        related_name='%(app_label)s_%(class)s_image',
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
        if self.redo_query or not self.pk:
            self.redo_query = False
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
            self.abstract = publication.abstract

        super(Publication, self).save(*args, **kwargs)

    def __str__(self):
        if len(self.title) >= 45:
            title = "{}...".format(self.title[:40])
        else:
            title = self.title

        return "{} - {} - {} - {} [{}]".format(self.year,
            self.first_author, self.journal, title, str(self.pmid),)

    class Meta:
        ordering = ('-year', '-month', '-day', 'first_author')


class PublicationSet(models.Model):

    name = models.CharField('name',
        help_text="Enter a unique name for this Publication Set. " \
                  "This won't be displayed on the site.",
        max_length=255,
        # primary_key=True,
        unique=True,
    )
    label = models.CharField('label',
        help_text='Enter a label for this Publication Set. ' \
                  'This may be displayed on the site.',
        max_length=255,
    )
    description = models.TextField('description',
        blank=True,
        help_text='Enter a description of this Publication Set.',
    )

    publications = models.ManyToManyField(Publication)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('label',)


class PublicationSetPlugin(CMSPlugin):
    publication_set = models.ForeignKey('cms_lab_publications.PublicationSet')

    def __str__(self):
        return self.publication_set.name
