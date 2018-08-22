"""
{{cookiecutter.project_label}} Setup
"""

import os
import re

from setuptools import setup, find_packages

VERSION = os.getenv('VERSION', '0.0.0')


# Read in the package names from requirements.txt,
# all of which should be required for the package to function
package_deps = None
with open('requirements.txt') as requirements_file:
    package_deps = frozenset([
        pkg for pkg in [re.split(r'[<>=]?', re.split(r'\s+', line)[0])[0] for line in
                        requirements_file.read().splitlines()]
        if pkg and pkg[0].isalpha()
    ])

setup(
    name='{{cookiecutter.application_name}}',
    version=VERSION,
    description='{{cookiecutter.project_label}} for SocialCode',
    author='SocialCode Engineering Team',
    author_email='devteam@socialcodeinc.com',
    url='http://www.socialcode.com',
    packages=find_packages(),
    classifiers=[
      'Framework :: Django',
      'Development Status :: 1 - Planning',
      'Environment :: Web Environment',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Intended Audience :: Developers',
      'Operating System :: OS Independent',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=package_deps,
    include_package_data=True,
    package_data={
      '{{cookiecutter.application_name}}': [
          'batch_job_definitions/*.tmpl',
          'fixtures/*.json',
          'migrations/*.py',
          'static/*'
      ]
    },
    zip_safe=False
)
