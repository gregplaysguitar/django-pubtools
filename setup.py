#!/usr/bin/env python
# coding: utf8

from setuptools import setup, find_packages

# avoid importing the module
exec(open('pubtools/_version.py').read())

setup(
    name='django-pubtools',
    version=__version__,
    description='A set of reusable base classes and helpers for django',
    long_description=open('readme.md').read(),
    author='Greg Brown',
    author_email='greg@gregbrown.co.nz',
    url='https://github.com/gregplaysguitar/django-pubtools',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['Django>=1.10', 'django-next-prev>=1.0'],
    keywords=['django', 'publishing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
)
