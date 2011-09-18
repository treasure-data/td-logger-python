#!/usr/bin/python

from distutils.core import setup

setup(
  name='td-logger',
  version='0.1',
  package_dir={'tdlog': 'tdlog'},
  packages=['tdlog'],
  install_requires=['msgpack-python'],
  author='Kazuki Ohta',
  author_email='k@treasure-data.com',
  url='https://github.com/treasure-data/td-logger-python',
  license='MIT'
)
