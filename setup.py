#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='mocksqlalchemy',
      version='0.1.2',
      description='A collection of mocks for unit testing code using the SQLAlchemy library.',
      author='Andy Levisay',
      author_email='levisaya@gmail.com',
      url='https://github.com/levisaya/mocksqlalchemy',
      download='https://github.com/levisaya/mocksqlalchemy/tarball/0.1.1',
      zip_safe=False,
      packages=find_packages(),
     )
