#!/usr/bin/env python
import pytest
import nose.tools as nt
from pathlib import Path
from jobcoin import util


def test_combine_url_success():
    url = 'http://test.com/'
    parameter = 'test.html'
    result = util.combine_url(url, parameter)
    nt.assert_true(result=='http://test.com/test.html')
