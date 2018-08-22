"""Client classes that communicate with other services"""
import logging
import looker_client
from urllib import parse

from django.conf import settings
from django.core.cache import cache
from oauthlib.oauth2 import BackendApplicationClient
from requests import (
    request,
    get,
    head,
    post,
    patch,
    put,
    delete,
    options,
)
from requests_oauthlib import OAuth1Session, OAuth2Session

from .utils import json_or_raise_for_status

LOGGER = logging.getLogger(__name__)

MAXIMUM_LOOKUP_LIMIT = 1000


def user_agent_string(func):
    """User Agent String decorator."""
    def decorator(*args, **kwargs):  # pylint: disable=missing-docstring
        headers = kwargs.pop('headers', {})
        headers.update({'User-Agent': settings.USER_AGENT_STRING})
        kwargs['headers'] = headers
        return func(*args, **kwargs)
    return decorator


class BaseAPIClient:
    """Base class for Socialcode API clients"""

    @property
    def default_netloc(self):
        "Retrieve default netloc."
        raise NotImplementedError()

    @property
    def default_proto(self):
        "Retrieve default protocol."
        return 'https'

    def modified_url(self, url):
        """Inject the appropriate ads netloc if unspecified."""
        url_parts = list(parse.urlsplit(url))
        if not url_parts[0]:
            url_parts[0] = self.default_proto

        if not url_parts[1]:
            url_parts[1] = self.default_netloc

        modified_url = parse.urlunsplit(url_parts)
        LOGGER.debug("requesting URI %s", modified_url)
        return modified_url


class APIClient(BaseAPIClient):
    """A simple client that implements the common HTTP methods"""
    def request(self, method, url, **kwargs):
        """
        Constructs and sends an HTTP or HTTPS Request, qualifying with netlocs and protocols as needed to make URL's
        absolute.

        Args:
            method: str. an HTTP method (e.g GET, POST)
            url: str. A relative or absolute URL. If relative, the URL will be qualified according to the default
            netloc and/or protocol for the APIClient.
            **kwargs: any valid kwarg for requests.Session.request

        Returns: requests.Response
        """
        return request(method, self.modified_url(url), **kwargs)

    @user_agent_string
    def get(self, url, **kwargs):
        """Sends a GET request."""
        return get(self.modified_url(url), **kwargs)

    @user_agent_string
    def options(self, url, **kwargs):
        """Sends a OPTIONS request."""
        return options(self.modified_url(url), **kwargs)

    @user_agent_string
    def head(self, url, **kwargs):
        """Sends a HEAD request."""
        return head(self.modified_url(url), **kwargs)

    @user_agent_string
    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request."""
        return post(self.modified_url(url), data, json, **kwargs)

    @user_agent_string
    def put(self, url, data=None, **kwargs):
        """Sends a PUT request."""
        return put(self.modified_url(url), data, **kwargs)

    @user_agent_string
    def patch(self, url, data=None, **kwargs):
        """Sends a PATCH request."""
        return patch(self.modified_url(url), data, **kwargs)

    @user_agent_string
    def delete(self, url, **kwargs):
        """Sends a DELETE request."""
        return delete(self.modified_url(url), **kwargs)


class AuthServiceClient(APIClient):
    """A Session with default urls for the authorization-service"""

    @property
    def default_netloc(self):
        return settings.SOCIALCODE_HOST

    def get_current_user(self, cookies):
        """
        Retrieve current user from authorization-service.
        Args:
            cookies: cookies that identify the user to authorization-service
        Returns: the current authenticated user
        {
          "type": "auth-user",
          "id": "91",
          "attributes": {
            "archived_on": null,
            "created_on": "2015-07-28T10:31:43Z",
            "email": "leonard@socialcodeinc.com",
            "first_name": "Leonard",
            "full_name": "Leonard Lu",
            "is_archived": false,
            "is_locked": false,
            "identity_provider": "GOOGLE",
            "image_url": "https://lh3.googleusercontent.com/-UqRu0TuwUKY/AAAAAAAAAAI/AAAAAAAAAGs/d-xJtGwBLzs/photo.jpg?sz=50",
            "last_login": "2018-04-19T00:21:48.818270Z",
            "last_name": "Lu",
            "modified_on": "2015-07-28T10:31:43Z",
            "password_reset_at": null,
            "status": "active"
          },
          "relationships": {
            "org": {
              "data": {
                "type": "auth-organization",
                "id": "2"
              }
            }
          },
          "links": {
            "self": "https://alpha.socialcodedev.com/api/auth/v1/user/91/"
          }
        }
        """
        response = self.get(settings.AUTHORIZATION_SERVICE_CURRENT_USER_ENDPOINT, cookies=cookies)
        return json_or_raise_for_status(response)['data']

    def get_user_authorizations(self, cookies):
        """
        Retrieve user's authorizations from authorization-service.
        Args:
            cookies: cookies that identify the user to authorization-service
        Returns: a list of authorizations
        [
            {
                "type": "auth-authorization",
                "id": "user:91:home-application:launch,read",
                "attributes": {
                    "resource_type": "home-application",
                    "is_restricted": False,
                    "resource_ids": null,
                    "scopes": ["launch", "read"]
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "auth-user",
                            "id": "91"
                        }
                    }
                }
            },
            {
                "type": "auth-authorization",
                "id": "user:91:auth-user:read",
                "attributes": {
                    "resource_type": "home-application",
                    "is_restricted": True,
                    "resource_ids": ["2", "91"],
                    "scopes": ["read"]
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "auth-user",
                            "id": "91"
                        }
                    }
                }
            }
        ]
        """
        response = self.get(settings.AUTHORIZATION_SERVICE_CURRENT_AUTHORIZATION_ENDPOINT, cookies=cookies)
        return json_or_raise_for_status(response)['data']


class SocialCodeAPISession(OAuth1Session, APIClient):
    """Base class for social code API sessions"""

    def __init__(self, platform, **kwargs):
        """Set session parameters"""
        self.platform = platform
        client_settings = self.client_settings()
        key, secret = None, None
        if client_settings:
            key = client_settings.get('key')
            secret = client_settings.get('secret')
        super(SocialCodeAPISession, self).__init__(key, secret, **kwargs)

    def client_settings(self):
        """Returns oauth key/secret pair for a given platform"""
        return settings.ADS_API_OAUTH[self.platform]

    @property
    def default_netloc(self):
        return settings.SOCIALCODE_HOST

    def request(self, method, url, **kwargs):
        """
        Construct and send an HTTP or HTTPS Request,
        qualifying with netlocs and protocols as needed to make URL's
        absolute.
        :param url: str. A relative or absolute URL. If relative,
        the URL will be qualified according to the default
        netloc and/or protocol for the APISession.
        :returns: requests.Response
        """
        response = super(
            SocialCodeAPISession, self
        ).request(method, self.modified_url(url), **kwargs)
        return json_or_raise_for_status(response)


def _get_api_cached_client(cache, constructor, platform):
    """
    Retrieve an appropriate API client
    """
    cache_key = constructor.cache_key

    if cache_key not in cache:
        cache[cache_key] = constructor(platform)

    return cache[cache_key]


def _create_api_cache(cache, constructor):
    """
    Create api-service cache
    """
    return lambda platform: _get_api_cached_client(cache, constructor, platform)



class KeychainAPISession(SocialCodeAPISession):
    """
    API session for Keychain
    """
    cache_key = settings.KEYCHAIN

    def get_facebook_platform_token(self, purpose='socialcode_ads_management'):
        """Retrieves Facebook token from Keychain"""
        url = settings.ADS_API_BASE_URI[settings.KEYCHAIN] + 'keys/'
        params = {
            'app__type': 'facebook',
            'purpose': purpose,
            'state':  1,
            'team_id': 1,
            'sort_by': 'name',
        }
        keys = self.get(url=url, params=params).get('objects')
        if keys:
            return keys[0].get('access_token')
        LOGGER.debug(f'No Facebook token in Keychain for Team(1) and Purpose({purpose})')
        return ''


def get_keychain_client():
    """
    Creates a Keychain API session client
    """
    _get_keychain_client = _create_api_cache({}, KeychainAPISession)
    return _get_keychain_client({{cookiecutter.project_name__clients__settings_service_name}})


class AuthServiceOAuth2Client(BaseAPIClient, OAuth2Session):
    """An OAuth2 authenticated client for the authorization-service that uses Basic Auth to acquire an access token.

    On initial writing this class does not automatically refresh its token. Since the
    authorization-service access tokens expire after 10 hours this does not affect any known use cases. If you expect
    your code to run long enough for the token to expire, then catch and handle TokenExpiredError"""

    def __init__(self):
        client = BackendApplicationClient(client_id=settings.AUTHORIZATION_SERVICE_CLIENT_ID)
        super(AuthServiceOAuth2Client, self).__init__(client=client)
        self.headers.update({'User-Agent': settings.USER_AGENT_STRING})
        self.acquire_token()

    @property
    def default_netloc(self):
        return settings.SOCIALCODE_HOST

    def request(self, method, url, **kwargs):
        return super(AuthServiceOAuth2Client, self).request(method, self.modified_url(url), **kwargs)

    def acquire_token(self):
        """Set and return an access token for the authorization-service"""
        return self.fetch_token(
            token_url=self.modified_url(settings.AUTHORIZATION_SERVICE_TOKEN_ENDPOINT),
            client_id=settings.AUTHORIZATION_SERVICE_CLIENT_ID,
            client_secret=settings.AUTHORIZATION_SERVICE_CLIENT_SECRET,
        )

    def get_email(self, user_id):
        """Return the email address of the given user id, from the authorization-service"""
        resp = self.get(settings.AUTHORIZATION_SERVICE_AUTHORIZATION_ENDPOINT % user_id, params={'include': 'user'})
        return json_or_raise_for_status(resp)['included'][0]['attributes']['email']
