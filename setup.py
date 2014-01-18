#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

readme = open('README.rst').read()

setup(
    name='backcall',
    version='0.1.0',
    description='Specifications for callback functions passed in to an API',
    long_description=readme,
    author='Thomas Kluyver',
    author_email='takowl@gmail.com',
    url='https://github.com/takluyver/backcall',
    packages=['backcall'],
    license="BSD",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)