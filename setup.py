#!/usr/bin/python

from distutils.core import setup
from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.md'))
desc = 'A Python logging handler for Treasure Data Cloud'

setup(
  name='td-logger',
  version='0.4',
  desciption=desc,
  long_description=open(README).read(),
  package_dir={'tdlog': 'tdlog'},
  packages=['tdlog'],
  install_requires=['msgpack-python'],
  author='Kazuki Ohta',
  author_email='k@treasure-data.com',
  url='https://github.com/treasure-data/td-logger-python',
  download_url='http://pypi.python.org/pypi/td-logger/',
  license='MIT',
  classifiers=[
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
  ]
)
