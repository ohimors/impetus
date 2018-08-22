"""
{{cookiecutter.project_label}} Dev Settings
"""
from {{cookiecutter.application_name}}.settings import *


DEBUG = True
LOGGING['handlers']['console']['level'] = 'DEBUG'
ENABLE_API_DOCS = True

# Enable Django REST Framework Browsable API Renderer
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
    'rest_framework.renderers.BrowsableAPIRenderer'
)

try:
    from .local_settings import *
except ImportError:
    pass
