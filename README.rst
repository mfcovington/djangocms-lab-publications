**************************
djangocms-lab-publications
**************************

``djangocms-lab-publications`` is a Django app for adding sets of scientific publications with PubMed metadata to a Django site with django CMS-specific features. It uses ``pubmed-lookup`` to query PubMed using PubMed IDs or PubMed URLs.

Source code is available on GitHub at `mfcovington/djangocms-lab-publications <https://github.com/mfcovington/djangocms-lab-publications>`_. Information about and source code for ``pubmed-lookup`` is available on GitHub at `mfcovington/pubmed-lookup <https://github.com/mfcovington/pubmed-lookup>`_.

.. contents:: :local:


Installation
============

**PyPI**

.. code-block:: sh

    pip install djangocms-lab-publications

**GitHub**

.. code-block:: sh

    pip install https://github.com/mfcovington/djangocms-lab-publications/releases/download/0.1.5/djangocms-lab-publications-0.1.5.tar.gz


Configuration
=============

- `Install django CMS and start a project <http://docs.django-cms.org/en/latest/introduction/install.html>`_, if one doesn't already exist.

  - Unless you use this app as part of `djangocms-lab-site <https://github.com/mfcovington/djangocms-lab-site>`_ or plan to style the app from scratch, you will want to choose the ``Use Twitter Bootstrap Theme`` option (when running ``djangocms``) and then edit the resulting ``templates/base.html``. This will add style that looks like Bootstrap 2. To use Bootstrap 3 styling, remove the following line for the ``bootstrap-theme.min.css`` stylesheet from ``templates/base.html``:

    .. code-block:: python

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.x.x/css/bootstrap-theme.min.css">


- Do the following in ``settings.py``:

  - Add ``cms_lab_publications`` and its dependencies to ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            'taggit',
            'taggit_helpers',
            'cms_lab_publications',
            'easy_thumbnails',
            'filer',
            'mptt',
        )


  - Add ``easy_thumbnail`` settings: 

    .. code-block:: python

        # For easy_thumbnails to support retina displays (recent MacBooks, iOS)
        THUMBNAIL_HIGH_RESOLUTION = True
        THUMBNAIL_QUALITY = 95
        THUMBNAIL_PROCESSORS = (
            'easy_thumbnails.processors.colorspace',
            'easy_thumbnails.processors.autocrop',
            'filer.thumbnail_processors.scale_and_crop_with_subject_location',
            'easy_thumbnails.processors.filters',
        )
        THUMBNAIL_PRESERVE_EXTENSIONS = ('png', 'gif')
        THUMBNAIL_SUBDIR = 'versions'


- If ``cms_lab_publications`` is used in a project served by Apache, a config directory must be created within the Apache user's home directory. This config directory is used by code within biopython's ``Bio.Entrez.Parser.DataHandler`` which is used by ``pubmed_lookup``, a dependency of ``cms_lab_publications``.

  .. code-block:: sh

      # In this snippet, the Apache user is 'www-data' and
      # the Apache user's home directory is '/var/www/'
      sudo su - root
      cd /var/www/
      chown :www-data
      chmod g+s 
      mkdir -p /var/www/.config/biopython/Bio/Entrez/DTDs


Migrations
==========

Create and perform ``cms_lab_publications`` migrations:

.. code-block:: sh

    python manage.py makemigrations cms_lab_publications
    python manage.py migrate


Usage
=====

- Start the development server:

.. code-block:: sh

    python manage.py runserver


- Visit: ``http://127.0.0.1:8000/``
- Create a CMS page.
- Insert the ``Publication Set Plugin`` into a placeholder field.


*Version 0.1.5*
