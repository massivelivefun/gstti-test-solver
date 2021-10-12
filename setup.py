# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='test_solver',
    version='0.1.0',
    description='Package to complete gstti tests quickly.',
    long_description=README,
    author='Matthew Lance Fuller',
    author_email='matthewlancefuller@gmail.com',
    url='https://github.com/massivelivefun/test_solver',
    license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
