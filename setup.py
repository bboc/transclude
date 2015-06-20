#!/usr/bin/env python
from setuptools import setup, find_packages

print find_packages()

setup(
    name = "transclude",
    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            'transclude = transclude:main',
        ],
    }

)
