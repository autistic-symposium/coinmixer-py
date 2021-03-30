# -*- coding: utf-8 -*-
"""
util.py

Implements util methods for other modules.
"""

import os
import sys
import uuid

from pathlib import Path
from dotenv import load_dotenv


def get_config(key, env_path=None):
    """Given a key, get the value from the env file.

    Arguments:
        key (str)
    """
    env_path = env_path or Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    value = os.getenv(key)

    if not value:
        print('📛 Please set {} in .env'.format(key))
        sys.exit(0)
    return value


def combine_url(url, parameter):
    """Ensures that a URL is well-composed.

    Arguments:
        url (str)
        parameter (str)
    """
    url = url.strip('/')
    return '{}/{}'.format(url, parameter)


def round_float(num):
    """Ensures that a string preserves desired precision when converted to float.
    Arguments:
        num (str)
    Returns:
        num (float)
    """
    try:
        return round(float(num), int(get_config('SIGNIFICANT_DIGITS')))
    except ValueError:
        print('📛 Value needs to be a number.')
        sys.exit(0)


def generate_deposit_address():
    """Creates a disposible hexadecimal address.

    Returns:
        hex address (str)
    """
    return uuid.uuid4().hex


def get_addresses_list(addresses):
    """Format a string of addresses.

    Arguments:
        addresses (str)
    Returns:
        addresses (list)
    """
    if not addresses:
        sys.exit(0)
    addresses = addresses.split()
    return [_.strip(',') for _ in addresses]


def is_close(a, b=0.0, rel_tol=1e-09, abs_tol=0.0):
    """Deals with float comparison.

    Arguments:
        a, b (floats)
    Returns:
        closeness between a and b (float)
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
