"""Utility methods for application-service"""
import logging

import itertools
from collections import Counter
from requests import HTTPError, Response


LOGGER = logging.getLogger(__name__)

def json_or_raise_for_status(response: Response):
    """
    Wrapper for response.raise_for_status which logs URL and response data.
    Args:
        response: a requests.Response object

    Returns:
        the result of response.json()
    """
    result = None
    json_parsing_error = False
    try:
        result = response.json()
    except Exception as e:
        json_parsing_error = e

    try:
        response.raise_for_status()
    except Exception:
        LOGGER.error("request failed.sc:%s|url:%s|text:%s", response.status_code, response.url, response.text)
        raise

    if json_parsing_error:
        LOGGER.error("could not parse response.sc:%s|url:%s|text:%s", response.status_code, response.url, response.text)
        http_error_msg = 'Error for url: {}'.format(response.url)
        raise HTTPError(http_error_msg, response=response) from json_parsing_error

    return result

