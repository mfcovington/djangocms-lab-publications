from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count

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


class MissingAttachmentListFilter(admin.SimpleListFilter):
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


class CurrentTagsListFilter(admin.SimpleListFilter):
    """
    Filter records by django-taggit tags for the current model only.
    Tags are sorted alphabetically.
    """
    title = 'Tags'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        model_tags = [tag.name for tag in
            TaggedItem.tags_for(model_admin.model)]
        model_tags.sort()
        return tuple([(tag, tag) for tag in model_tags])

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(tags__name=self.value())


@admin.register(Publication)
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
        'has_pdf',
        'has_supplemental',
        'has_image',
    )
    list_filter = (
        MissingAttachmentListFilter,
        CurrentTagsListFilter,
        'journal',
        'year',
    )
    search_fields = (
        'abstract',
        'authors',
        'journal',
        'title',
    )

    def has_pdf(self, obj):
        return obj.pdf is not None
    has_pdf.boolean = True

    def has_supplemental(self, obj):
        return obj.supplemental_pdf is not None
    has_supplemental.boolean = True

    def has_image(self, obj):
        return obj.image is not None
    has_image.boolean = True


@admin.register(PublicationSet)
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

    fieldset_bulk = ('Add Publications in Bulk', {
        'fields': [
            'bulk_pubmed_query',
        ],
    })

    fieldsets = [
        fieldset_publication_set,
        fieldset_bulk,
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
        'number_of_publications',
        'searchable',
    )
    list_filter = (
        CurrentTagsListFilter,
    )

    search_fields = (
        'name',
        'label',
        'description',
    )

    def queryset(self, request):
        queryset = super().queryset(request)
        queryset = queryset.annotate(pub_count=Count('publications'))
        return queryset

    def number_of_publications(self, obj):
        return obj.pub_count
    number_of_publications.admin_order_field = 'pub_count'
