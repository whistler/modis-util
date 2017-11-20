# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='modis-util',
    version='0.1.0',
    description='Modis-util is a tool to make it easy to search and download MODIS data from AWS',
    long_description=readme,
    author='Ibrahim Muhammad',
    author_email='ibmmmm@gmail.com',
    url='https://github.com/whistler/modis-util',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
       'boto3>=1.4.7',
       'pandas>=0.21.0'
    ]
)