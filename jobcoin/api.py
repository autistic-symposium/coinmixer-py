# -*- coding: utf-8 -*-
"""
api.py

This module implements a client for Jobcoin API RESTful endpoints.
All requests calls are handled in this module.
"""

import sys
import requests

import jobcoin.util as util


def _get_request(url):
    """Sends a GET request to the given URL.

    Parameters:
        url (str)
    Returns:
        response (str)
    """
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as e:
        print('📛 GET request error: {}:'.format(e))
        sys.exit(0)


def _post_request(url, payload):
    """Sends a POST request to the given URL and payload.

    Parameters:
        url (str)
        payload (dict)
    Returns:
        response (str)
    """
    try:
        return requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        print('📛 POST request error: {}:'.format(e))
        sys.exit(0)


def get_balance(address):
    """Gets the balance from a given address.

    Parameters:
        address (str)
    Returns:
        balance (float): unused address returns a balance of 0
    """

    url = util.combine_url(util.get_config('API_ADDRESS_URL'), address)
    response = _get_request(url)

    if response.status_code == 200:
        data = response.json()

        try:
            return util.round_float(data['balance'])
        except KeyError as e:
            print('📛 Could not get balance from {}: '.format(address),
                  'Response is not well-formatted: {}'.format(e))

    else:
        print('📛 Could not get balance from {}:'.format(address),
              'status code {}'.format(response.status_code))
        sys.exit(0)


def get_transactions():
    """Gets a list of all the transations in Jobcoin.

    Returns:
        transactions (list of dicts)
    """
    # NOTE: The list of transactions might become very large with time.
    # if no check is done in the server, an enhancement would add this check,
    # sort by timestamp, or truncate after a certain size limit.

    url = util.get_config('API_TRANSACTIONS_URL')
    response = _get_request(url)

    if response.status_code == 200:
        return response.json()

    else:
        print('📛 Could not get transaction list: ',
              'status code {status}'.format(status=response.status_code))
        sys.exit(0)


def post_transaction(from_address, to_address, amount):
    """Issue a transaction between two given address and a given amount.

    Input Arguments:
        from_address (str)
        to_address (str)
        amount (str)
    Returns:
        status (str)
    """

    url = util.get_config('API_TRANSACTIONS_URL')
    payload = {
                'fromAddress': from_address,
                'toAddress': to_address,
                'amount': amount
             }
    response = _post_request(url, payload)

    if response.status_code == 422:
        print('📛 Could not post transaction: Insufficient funds!')
        sys.exit(0)
    elif response.status_code == 400:
        print('📛 Could not post transaction: Amount must be over 0!')
        sys.exit(0)
    elif response.status_code != 200:
        print('📛 Could not post transaction: ',
              'status code {}'.format(response.status_code))
        sys.exit(0)
