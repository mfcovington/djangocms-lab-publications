from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.toolbar.items import Break, SubMenu
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK


@toolbar_pool.register
class PublicationSetToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(
            ADMIN_MENU_IDENTIFIER, _('Apps')
        )

        position = admin_menu.get_alphabetical_insert_position(
            _('Publication Set'),
            SubMenu
        )

        if not position:
            position = admin_menu.find_first(
                Break,
                identifier=ADMINISTRATION_BREAK
            ) + 1
            admin_menu.add_break('custom-break', position=position)

        publication_set_menu = admin_menu.get_or_create_menu(
            'publication-set-menu',
            _('Publication Set ...'),
            position=position
        )

        url_change = reverse('admin:cms_lab_publications_publication_changelist')
        url_addnew = reverse('admin:cms_lab_publications_publication_add')
        publication_set_menu.add_sideframe_item(_('Edit Publications'), url=url_change)
        publication_set_menu.add_modal_item(_('Add New Publication'), url=url_addnew)
        publication_set_menu.add_break()

        url_change = reverse('admin:cms_lab_publications_publicationset_changelist')
        url_addnew = reverse('admin:cms_lab_publications_publicationset_add')
        publication_set_menu.add_sideframe_item(_('Edit Publication Sets'), url=url_change)
        publication_set_menu.add_modal_item(_('Add New Publication Set'), url=url_addnew)
