from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Publication, PublicationSet
from taggit.models import TaggedItem


class PublicationInline(admin.TabularInline):
    model = PublicationSet.publications.through
    extra = 3
    verbose_name = "Associated Publication"
    verbose_name_plural = "Associated Publications"
    ordering = ('-publication__year',)


class PublicationSetInline(admin.TabularInline):
    model = PublicationSet.publications.through
    extra = 1
    verbose_name = "Associated Publication Set"
    verbose_name_plural = "Associated Publication Sets"
    ordering = ('publicationset__name',)


class TaggedItemInline(GenericTabularInline):
    model = TaggedItem
    verbose_name = "Tag"
    verbose_name_plural = "Tags"
    ordering = ('tag__name',)


class PublicationAdmin(admin.ModelAdmin):

    fieldset_pubmed_query = ('PubMed Query', {
        'fields': [
            'pmid',
            'pubmed_url',
            'mini_citation',
            'redo_query',
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
        fieldset_pubmed_metadata,
        fieldset_files,
    ]

    inlines = [
        PublicationSetInline,
        TaggedItemInline,
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
    )
    list_filter = (
        'tags',
        'journal',
        'year',
    )
    search_fields = (
        'abstract',
        'authors',
        'journal',
        'title',
    )

admin.site.register(Publication, PublicationAdmin)


class PublicationSetAdmin(admin.ModelAdmin):

    fieldset_publication_set = ('Publication Set', {
        'fields': [
            'name',
            'label',
            'description',
            'pagination',
            'searchable',
        ],
    })

    fieldsets = [
        fieldset_publication_set,
    ]

    inlines = [
        PublicationInline,
        TaggedItemInline,
    ]

    save_on_top = True

    list_display = (
        'name',
        'label',
        'description',
        'pagination',
        'searchable',
    )
    list_filter = (
        'tags',
    )

    search_fields = (
        'name',
        'label',
        'description',
    )

admin.site.register(PublicationSet, PublicationSetAdmin)
