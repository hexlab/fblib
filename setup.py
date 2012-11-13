#!/usr/bin/env python
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(name='fblib',
    version='0.9',
    description='Alternative version of Facebook Python SDK',
    long_description=open('README.rst').read(),
    author='Kirill Karmadonov',
    author_email='kirill@live.com',
    url='https://github.com/0xKirill/fblib',
    install_requires=['requests==0.14.1'],
    packages=['fblib'],
    package_dir={'fblib': 'fblib'},
    include_package_data=True,
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ])
