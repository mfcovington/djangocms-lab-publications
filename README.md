# CMS Lab Publications

CMS Lab Publications is a Django app for adding sets of scientific publications with PubMed metadata to a Django site with django CMS-specific features.

<!-- Detailed documentation is in the "docs" directory. -->

## Quick start

- Install `djangocms-lab-publications` from GitHub:

    ```sh
    pip install https://github.com/mfcovington/djangocms-lab-publications/releases/download/0.1.2/djangocms-lab-publications-0.1.3.tar.gz
    ```

- Edit the project's `settings.py` file.

    - Add `cms_lab_publications` and its dependencies to your `INSTALLED_APPS` setting:

        ```python
        INSTALLED_APPS = (
            ...
            'taggit',
            'cms_lab_publications',
            'easy_thumbnails',
            'filer',
            'mptt',
        )
        ```

    - Specify your media settings, if not already specified:

        ```python
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        ```

    - Add `filer` and `easy_thumbnail` settings: 

        ```python
        # For filer's Django 1.7 compatibility
        MIGRATION_MODULES = {
            ...
            'filer': 'filer.migrations_django',
        }

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
        ```

- Run `python manage.py makemigrations cms_lab_publications` to create the `cms_lab_publications` migrations.

- Run `python manage.py migrate` to create the `cms_lab_publications` models.

- If `cms_lab_publications` is used in a project served by Apache, a config directory must be created within the Apache user's home directory. This config directory is used by code within biopython's `Bio.Entrez.Parser.DataHandler` which is used by `pubmed_lookup`, a dependency of `cms_lab_publications`.

    ```sh
    # In this snippet, the Apache user is 'www-data' and
    # the Apache user's home directory is '/var/www/'
    sudo su - root
    cd /var/www/
    chown :www-data
    chmod g+s 
    mkdir -p /var/www/.config/biopython/Bio/Entrez/DTDs
    ```

- Start the development server (`python manage.py runserver`) and visit http://127.0.0.1:8000/

- Create a CMS page and insert the `Publication Set Plugin` into a placeholder field.

*Version 0.1.3*
