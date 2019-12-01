#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='dataframemt',
    version='0.4.0',
    description="Extra Python modules to deal with dataframes for Minh-Tri Pham",
    author=["Minh-Tri Pham"],
    packages=find_packages(),
    install_requires=[
        'sqlmt>=0.3.9',
    ],
)
