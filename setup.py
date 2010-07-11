#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="Pest",
    version="1.0",
    description="Auto tester for python",
    packages = ['pest'],
    author="Chuck Collins",
    author_email="chuck.collins@gmail.com",
    scripts=['pest/pester'],
    install_requires=['pyobjc-framework-FSEvents','growl-py'],
    url="http://github.com/ccollins/pest",
    data_files=[('images', ['pest/images/fail.png', 'pest/images/pass.png', 'pest/images/pending.png'])]
)