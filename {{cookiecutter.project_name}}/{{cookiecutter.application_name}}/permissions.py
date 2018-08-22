"""Django REST Framework Permissions for application"""
import logging

from rest_framework import permissions

LOGGER = logging.getLogger(__name__)


def has_scope_for_resource(authorizations, resource_type, resource_id, scope):
    """Check if the given Type, Id and Scope exist in the provided Authorizations"""
    if not authorizations:
        return False

    for authorization in authorizations:
        attributes = authorization['attributes']
        has_resource_id = not attributes['is_restricted'] or resource_id in attributes['resource_ids']
        if attributes['resource_type'] == resource_type and has_resource_id and scope in attributes['scopes']:
            return True
    return False


def can_launch_{{cookiecutter.application_name}}(authorizations):
    """Check if the given authorizations have a Permission to launch service"""
    return has_scope_for_resource(
        authorizations=authorizations,
        resource_type='home-application',
        resource_id='{{cookiecutter.project_name__permissions__authorization_resource_id}}',
        scope='launch',
    )


class {{cookiecutter.project_name__application_service_name__common}}Permission(permissions.BasePermission):
    """Django REST Framework Permission for discovery-service"""
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return can_launch_discovery_service(request.auth)

    def has_object_permission(self, request, view, obj):
        """
        Return True if the request is safe (read-only), or the request user is the same as the object owner
        Otherwise return False
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not hasattr(obj, 'get_owner_id'):
            return False
        return int(request.user.id) == obj.get_owner_id()
