#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="Pest",
    version="0.2",
    packages = ['pest'],
    author="Chuck Collins",
    author_email="chuck.collins@gmail.com",
    scripts=['pest/pester'],
    install_requires=['pyobjc-framework-FSEvents','growl-py']
)