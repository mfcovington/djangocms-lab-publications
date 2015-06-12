import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requires = [
    "Django>=1.7.7,<1.8",
    "django-cms>=3.0",
    "django-filer>=0.9.9",
    "django-taggit>=0.14.0",
    "django-taggit-helpers>=0.1.1",
    "pubmed-lookup>=0.1.1",
]

setup(
    name='djangocms-lab-publications',
    version='0.1.3',
    packages=['cms_lab_publications'],
    include_package_data=True,
    license='BSD License',
    description='A Django app for adding sets of scientific publications with PubMed metadata to a Django site with django CMS-specific features',
    long_description=README,
    url='https://github.com/mfcovington/djangocms-lab-publications',
    author='Michael F. Covington',
    author_email='mfcovington@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=install_requires,
)
