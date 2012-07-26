#!/usr/bin/env python
from setuptools import setup

setup(
    name='sphinx-jsapidoc',
    version='0.1.1',
    description='Documentation generator for javascript files for sphinx output.',
    author='Oliver Wilkerson, Nuu Logic LLC',
    author_email='oliver.wilkerson@nuulogic.com',
    url='http://github.com/nuulogic/sphinx-jsapidoc/',
    
    # what to install
    packages=['sphinxjsapidoc'],
    
    # searches and classifications
    keywords='sphinx,autodoc,sphinx-apidoc,sphinx-autodoc,docutils,documentation,docs,jsdoc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: TBD',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
    ],
    
    # dependencies
    install_requires=[
        'docutils',
        'Sphinx',
    ],

    scripts=[
        'sphinx-jsapidoc'
    ],
)
