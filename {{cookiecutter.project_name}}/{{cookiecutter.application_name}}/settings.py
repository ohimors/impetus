"""
Application Settings
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Secrets are overwritten on servers and should not be checked into repos.
SECRET_KEY = 'django_secret_key_placeholder'
VERSION = os.getenv('VERSION', '0.0.0')

ALLOWED_HOSTS = ['*']

SC_ENV = 'alpha'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'rest_framework_swagger',
    '{{cookiecutter.application_name}}',
    
)

STATIC_URL = '/static/'
STATIC_ROOT = '/var/{{cookiecutter.application_name}}/static/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Django session settings
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_NAME = "bouncer"
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(threadName)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        '{{cookiecutter.application_name}}': {
            'handlers': ['sentry'],
            'level': 'DEBUG',
        },
        'sentry.errors': {
            'level': 'DEBUG',
        },
        # Uncomment to debug queries/performance
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # },
    }
}

ROOT_URLCONF = '{{cookiecutter.application_name}}.urls'
WSGI_APPLICATION = '{{cookiecutter.application_name}}.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{cookiecutter.docker_compose__database_name__common}}',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': '{{cookiecutter.docker_compose__mysql_user__common}}',
        'PASSWORD': 'edoclaicos',
        'CHARSET': 'utf8mb4',
        'COLLATION': 'utf8mb4_general_ci',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES'
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        '{{cookiecutter.application_name}}.authentication.AuthorizationServiceAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'DEFAULT_PAGINATION_CLASS':
        '{{cookiecutter.application_name}}.pagination.PageNumberPagination',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        '{{cookiecutter.application_name}}.permissions.{{cookiecutter.project_name__application_service_name__common}}Permission',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'ORDERING_PARAM': 'sort',
    'PAGE_SIZE': 20,
}
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = False
JSON_API_FORMAT_KEYS = 'underscore'

USER_AGENT_STRING = '{{cookiecutter.project_name}}/{}'.format(VERSION)

AUTHORIZATION_SERVICE_CURRENT_USER_ENDPOINT = '/api/auth/v1/user/current/'
AUTHORIZATION_SERVICE_AUTHORIZATION_ENDPOINT = '/api/auth/v1/user/%s/authorization/'
AUTHORIZATION_SERVICE_CURRENT_AUTHORIZATION_ENDPOINT = AUTHORIZATION_SERVICE_AUTHORIZATION_ENDPOINT % 'current'
AUTHORIZATION_SERVICE_TOKEN_ENDPOINT = '/api/auth/v1/token/'

SOCIALCODE_HOST = 'alpha.socialcodedev.com'

{{cookiecutter.settings_application_name}} = '{{cookiecutter.project_name}}'
KEYCHAIN = 'keychain'
ADS_API_BASE_URI = {
    KEYCHAIN: '/api/keychain/v2/',
}

# Set up ads SocialCode OAuth Clients
ADS_API_OAUTH = {
    '{{cookiecutter.project_name}}': {
        'key': 'client-key-from-databag',
        'secret': 'client-secret-from-databag'
    },
}


# Authorization Service settings
AUTHORIZATION_SERVICE_CLIENT_ID = 'client-id-from-databag'
AUTHORIZATION_SERVICE_CLIENT_SECRET = 'client-secret-from-databag'
