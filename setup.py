#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

from fblib import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requirements = ['requests']

setup(name='fblib',
      version=".".join(map(str, __version__)),
      description='Alternative version of Facebook Python SDK',
      long_description=read('README.rst'),
      author='Kirill Karmadonov',
      author_email='kirill@live.com',
      url='https://github.com/0xKirill/fblib',
      install_requires=['requests==2.19.1'],
      packages=find_packages(exclude=['tests']),
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
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ])
