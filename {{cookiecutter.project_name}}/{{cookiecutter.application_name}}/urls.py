"""Application Service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import (
    include,
    path,
)
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from . import views


router = DefaultRouter(trailing_slash=True)
slashless_router = DefaultRouter(trailing_slash=False)
slashless_router.registry = router.registry[:]

urlpatterns = [
    path('api/{{cookiecutter.project_name}}/v1/', include(router.urls)),
    path('api/{{cookiecutter.project_name}}/v1/', include(slashless_router.urls)),

    path('ping/', views.ping),
    path('version/', views.version),
]

# enable swagger api docs
if getattr(settings, 'ENABLE_API_DOCS', False):
    schema_view = get_swagger_view(title='{{cookiecutter.project_label}}')
    urlpatterns += [path('api/{{cookiecutter.project_name}}/docs/', schema_view)]
