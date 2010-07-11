#!/usr/bin/env python
from setuptools import setup
setup(
    name="Pest",
    version="1.0",
    packages = ['pest'],
    scripts=['pest/pester'],
    package_data = {'pest': ['images/*.png'],},
    data_files=[('images', ['pest/images/fail.png', 'pest/images/pass.png', 'pest/images/pending.png'])],
    install_requires=['pyobjc-framework-FSEvents','growl-py'],
    description="Auto tester for python",
    author="Chuck Collins",
    author_email="chuck.collins@gmail.com",
    url="http://github.com/ccollins/pest",
)