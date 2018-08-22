"""Authentication module for application"""
from django.contrib.auth.models import AnonymousUser
from requests import HTTPError
from rest_framework.authentication import BaseAuthentication

from .clients import AuthServiceClient


class BaseUser(AnonymousUser):
    """An identifiable Django user"""
    is_active = True
    is_authenticated = True
    is_anonymous = False

    # pylint: disable=unused-argument
    def __init__(self, user_id, *args, **kwargs):
        self.id = self.pk = self.username = user_id

    def __str__(self):
        return self.username

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(id)


class SocialCodeUser(BaseUser):
    """
    A Django user identified by authorization-service id.
    Use with AuthorizationServiceAuthentication
    """

    # pylint: disable=unused-argument
    def __init__(self, user_id, *args, **kwargs):
        user_id = kwargs['auth_service_user']['id']
        super(SocialCodeUser, self).__init__(user_id, *args, **kwargs)
        self.username = 'SocialCodeUser: {}'.format(self.id)
        self.auth_service_user = kwargs['auth_service_user']


class AuthorizationServiceAuthentication(BaseAuthentication):
    """
    Fetch authorizations from authorization-service
    """
    def authenticate(self, request):
        """
        Try to authenticate the request with SocialCode's authorization service.
        :param request:
        :return: user, authorizations tuple
        """
        try:
            client = AuthServiceClient()
            auth_service_user = client.get_current_user(request.COOKIES)
            authorizations = client.get_user_authorizations(request.COOKIES)
        except HTTPError:
            return None

        return SocialCodeUser(user_id=auth_service_user['id'], auth_service_user=auth_service_user), authorizations
