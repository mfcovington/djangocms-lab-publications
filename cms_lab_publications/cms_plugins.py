import collections
import operator

from django.core.urlresolvers import reverse

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Publication, PublicationSet, PublicationSetPlugin


class CMSPublicationSetPlugin(CMSPluginBase):
    model = PublicationSetPlugin
    module = "Lab Plugins"
    name = "Publication Set Plugin"
    render_template = "cms_lab_publications/plugin.html"

    def render(self, context, instance, placeholder):
        pub_set_tags = {}
        pub_set = instance.publication_set.publications.all()
        for pub in pub_set:
            for tag in pub.tags.all():
                pub_set_tags[tag.id] = tag.name
        pub_set_tags = collections.OrderedDict(sorted(pub_set_tags.items(), key=operator.itemgetter(1)))

        context.update({
            'instance': instance,
            'pub_set_tags': pub_set_tags,
        })

        menu = context['request'].toolbar.get_or_create_menu('publication-set-menu','Publication Set')

        url_change = reverse('admin:cms_lab_publications_publication_changelist')
        url_addnew = reverse('admin:cms_lab_publications_publication_add')
        menu.add_sideframe_item('Edit Publications', url=url_change)
        menu.add_modal_item('Add New Publication', url=url_addnew)
        menu.add_break()

        url_change = reverse('admin:cms_lab_publications_publicationset_changelist')
        url_addnew = reverse('admin:cms_lab_publications_publicationset_add')
        menu.add_sideframe_item('Edit Publication Sets', url=url_change)
        menu.add_modal_item('Add New Publication Set', url=url_addnew)

        return context


plugin_pool.register_plugin(CMSPublicationSetPlugin)
