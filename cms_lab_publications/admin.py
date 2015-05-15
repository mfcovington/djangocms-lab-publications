from django.contrib import admin

from .models import Publication, PublicationSet


class PublicationInline(admin.TabularInline):
    model = PublicationSet.publications.through
    extra = 3
    verbose_name = "Publication"
    verbose_name_plural = "Publications"
    ordering = ('-publication__year',)


class PublicationAdmin(admin.ModelAdmin):

    fieldset_pubmed_query = ('PubMed Query', {
        'fields': [
            'pmid',
            'pubmed_url',
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
            'redo_query',
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

    list_display = (
        'pmid',
        'year',
        'first_author',
        'last_author',
        'journal',
        'title',
    )
    list_filter = (
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
        ],
    })

    fieldsets = [
        fieldset_publication_set,
    ]

    inlines = [
        PublicationInline,
    ]

    list_display = (
        'name',
        'label',
        'description',
    )

    search_fields = (
        'name',
        'label',
        'description',
    )

admin.site.register(PublicationSet, PublicationSetAdmin)
