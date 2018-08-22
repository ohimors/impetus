"""
Application Service Views
"""

from django.conf import settings
from django.http import HttpResponse

def ping(request):  # pylint: disable=unused-argument
    """Health check for determining if the server is available."""
    response_content = '<html><body>OK</body></html>'
    return HttpResponse(response_content, content_type='text/html')


def version(request):  # pylint: disable=unused-argument
    """Return the application version string."""
    response_content = '<html><body>%s</body></html>' % settings.VERSION
    return HttpResponse(response_content, content_type='text/html')

