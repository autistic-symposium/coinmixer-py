#!/usr/bin/env python
import pytest
import requests
import nose.tools as nt
from jobcoin import api


@pytest.fixture
def response_get_balance(address):
    return requests.get('http://jobcoin.gemini.com/aide-sports/api/addresses/{}'.format(address))


def test_get_balance_200():
    response = response_get_balance('Alice')
    nt.assert_true(response.ok)


def test_get_balance_response_not_none():
    response = response_get_balance('Alice')
    nt.assert_is_not_none(response)


def test_get_balance_response_empty_address():
    response = response_get_balance('')
    nt.assert_true(response.status_code==404)
