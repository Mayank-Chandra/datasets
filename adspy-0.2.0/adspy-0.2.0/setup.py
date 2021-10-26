import os
from setuptools import setup, find_packages
version = '0.2.0'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read() + 'nn'
setup(name='adspy',
      version=version,
      description=("Simple bibtex tools for use with ADS."),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords='data',
      author='Samuel Skillman <samskillman@gmail.com>',
      license='GPLv3',
      packages=find_packages(),
      )
