from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count

from .models import Publication, PublicationSet
from taggit.models import TaggedItem
from taggit_helpers import (TaggitCounter, TaggitListFilter,
    TaggitTabularInline)


class PublicationSetInline(admin.TabularInline):
    model = PublicationSet.publications.through
    extra = 1
    verbose_name = "Associated Publication Set"
    verbose_name_plural = "Associated Publication Sets"
    ordering = ('publicationset__name',)


class MissingAttachmentListFilter(admin.SimpleListFilter):
    """
    Filter Publication records by the presence of attached files.
    """
    title = 'Missing Attachments'
    parameter_name = 'attachment'

    def lookups(self, request, model_admin):
        return (
            ('-pdf', 'Missing PDF'),
            ('-sup', 'Missing Supplemental'),
            ('-image', 'Missing Image'),
            ('+pdf', 'Has PDF'),
            ('+sup', 'Has Supplemental'),
            ('+image', 'Has Image'),
        )

    def queryset(self, request, queryset):
        if self.value() == '-pdf':
            return queryset.filter(pdf=None)
        if self.value() == '-sup':
            return queryset.filter(supplemental_pdf=None)
        if self.value() == '-image':
            return queryset.filter(image=None)
        if self.value() == '+pdf':
            return queryset.exclude(pdf=None)
        if self.value() == '+sup':
            return queryset.exclude(supplemental_pdf=None)
        if self.value() == '+image':
            return queryset.exclude(image=None)


class BulkPubMedQueryStatusFilter(admin.SimpleListFilter):
    """
    Filter Publication Set records by whether its Bulk PubMed Query failed.
    """
    title = 'Bulk PubMed Query Status'
    parameter_name = 'query_status'

    def lookups(self, request, model_admin):
        return (
            ('ok', 'OK'),
            ('failed', 'Failed'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'ok':
            return queryset.filter(bulk_pubmed_query='')
        elif self.value() == 'failed':
            return queryset.exclude(bulk_pubmed_query='')


@admin.register(Publication)
class PublicationAdmin(TaggitCounter, admin.ModelAdmin):

    fieldset_pubmed_query = ('PubMed Query', {
        'fields': [
            'pmid',
            'pubmed_url',
            'mini_citation',
            'redo_query',
            'no_query',
        ],
    })

    fieldset_files = ('Files', {
        'fields': [
            'pdf',
            'supplemental_pdf',
            'image',
        ],
    })

    fieldset_pubmed_metadata = ('Auto-generated PubMed Metadata', {
        'fields': [
            'citation',
            'url',
            'title',
            'authors',
            'first_author',
            'last_author',
            'journal',
            'year',
            'month',
            'day',
            'abstract',
        ],
        'classes': [
            'collapse',
        ],
    })

    fieldsets = [
        fieldset_pubmed_query,
        fieldset_files,
        fieldset_pubmed_metadata,
    ]

    inlines = [
        TaggitTabularInline,
        PublicationSetInline,
    ]

    readonly_fields = ('mini_citation',)
    save_on_top = True

    list_display = (
        'pmid',
        'year',
        'first_author',
        'last_author',
        'journal',
        'title',
        'has_pdf',
        'has_supplemental',
        'has_image',
        'number_of_publication_sets',
        'taggit_counter',
    )
    list_filter = (
        MissingAttachmentListFilter,
        TaggitListFilter,
        'journal',
        'year',
    )
    search_fields = (
        'abstract',
        'authors',
        'pmid',
        'journal',
        'title',
        'year',
    )

    def has_pdf(self, obj):
        return obj.pdf is not None
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF?'

    def has_supplemental(self, obj):
        return obj.supplemental_pdf is not None
    has_supplemental.boolean = True
    has_supplemental.short_description = 'Supplement?'

    def has_image(self, obj):
        return obj.image is not None
    has_image.boolean = True
    has_image.short_description = 'Image?'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(pub_set_count=Count('publicationset'))
        return queryset

    def number_of_publication_sets(self, obj):
        return obj.pub_set_count
    number_of_publication_sets.admin_order_field = 'pub_set_count'
    number_of_publication_sets.short_description = '# of Pub Sets'


@admin.register(PublicationSet)
class PublicationSetAdmin(TaggitCounter, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        Allow Bulk PubMed Query to update publications field on admin form.
        """
        if obj.bulk_pubmed_query:
            obj.publications = ''
            obj.perform_bulk_pubmed_query()
            form.cleaned_data['publications'] = form.cleaned_data['publications'] \
                                              | obj.publications.all()

        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('cms_lab_publications/css/admin-publication-filter.css',)
        }

    fieldset_publication_set = ('Publication Set', {
        'fields': [
            'name',
            'label',
            'description',
            'pagination',
            'searchable',
        ],
    })

    fieldset_bulk = ('Add Publications in Bulk', {
        'fields': [
            'bulk_pubmed_query',
        ],
    })

    fieldset_publications = ('Publications', {
        'fields': [
            'publications',
        ],
    })

    fieldsets = [
        fieldset_publication_set,
        fieldset_bulk,
        fieldset_publications,
    ]

    filter_vertical = ['publications']

    inlines = [
        TaggitTabularInline,
    ]

    save_on_top = True

    list_display = (
        'name',
        'label',
        'description',
        'number_of_publications',
        'pagination',
        'searchable',
        'is_bulk_pubmed_query_ok',
        'taggit_counter',
    )
    list_filter = (
        BulkPubMedQueryStatusFilter,
        TaggitListFilter,
    )

    search_fields = (
        'name',
        'label',
        'description',
    )

    def is_bulk_pubmed_query_ok(self, obj):
        return obj.bulk_pubmed_query == ''
    is_bulk_pubmed_query_ok.boolean = True
    is_bulk_pubmed_query_ok.short_description = 'Query OK?'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(pub_count=Count('publications'))
        return queryset

    def number_of_publications(self, obj):
        return obj.pub_count
    number_of_publications.admin_order_field = 'pub_count'
    number_of_publications.short_description = '# of Publications'
