"""
{{cookiecutter.project_label}} App Config
"""

from django.apps import AppConfig


class {{cookiecutter.project_name__application_service_name__common}}Config(AppConfig):
    """ {{cookiecutter.project_label}} Configuration """
    name = '{{cookiecutter.application_name}}'
    verbose_name = '{{cookiecutter.project_label}}'
