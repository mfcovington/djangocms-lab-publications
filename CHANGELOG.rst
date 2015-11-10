Revision History
================

0.1.5 2015-11-09

- Fix styling of vertical filter selector buttons and boxes in response to changes in ``djangocms-admin-style``
- Add bottom margin to non-paginated publication lists
- Remove 'Abstract' button from modal
- Resolve Django 1.8 warnings
- Update README with more complete and accurate instructions


0.1.4 2015-06-24

- Allow manual entry of Publications that don't have a PubMed ID
- Use django-taggit-helpers in admin
- Rename deprecated queryset method
- Configure bumpversion & wheel for easier distribution
- Convert README and changelog to reStructuredText for distribution via PyPI
- Minor changes to admin interface

  - Change pagination description to 'pubs per page'
  - Add/update help text for 'tags' and 'pagination'


0.1.3 2015-06-03

- Allow bulk PubMed queries for a Publication Set
- Allow a Publication Set to be created without publications
- Default to no pagination (hides page '1' button for short publication sets)
- Set default Publication Set label to 'Publications'
- Admin improvements

  - Publication Admin

    - Reorder Publication Admin's inlines
    - Add year and PubMed ID to Publication Admin search field
    - Display (and sort by) # of Publication Sets in Publication Admin

  - Publication Set Admin

    - In Publication Set Admin, move publications from a tabular inline to a vertical filter
    - Reorder Publication Set Admin's list display items
    - Filter Publication Set records by whether its Bulk PubMed Query failed
    - Display whether a Publication Set's Bulk PubMed Query status is OK

  - Other

    - Update and improve layout of help text
    - Add short descriptions for custom list display items
    - Add docstring for MissingAttachmentListFilter


0.1.2 2015-05-27

- Expand documentation for installation and configuration
- Add mini_citation field to Publication

  - Helps identify publication when in edit mode (without expanding PubMed Metadata fieldset)
  - Helps naming associated files (PDF, Supplemental, and Image) by providing a base name
  - Bumps ``pubmed-lookup`` dependency to version 0.1.1

- Many improvements to Publication and Publication Set Admins

  - Rearrange Publication Admin fieldsets
  - Add PublicationSetInline to PublicationAdmin
  - Add save button across tops of Publication and Publication Set Admins
  - Now Powered by Blackina
  - Display whether a record has PDF/Supp/Image attachments in Publication Admin
  - Filter PublicationAdmin by missing/existing attachments
  - Filter Publication and Publication Set Admins by tags for the current model only
  - Show (and sort by) 'number of publications' for records in Publication Set Admin


0.1.1 2015-05-23

- Allow multiple Publication Set plugins per page
- Use Publication Set's name, not label, for ``__str__`` and ordering


0.1.0 2015-05-22

- A Django app for adding sets of scientific publications with PubMed metadata to a Django site with django CMS-specific features
