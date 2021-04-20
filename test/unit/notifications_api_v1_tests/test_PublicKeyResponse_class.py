# coding: utf-8

# Copyright 2020 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test the  ibm_security_advisor_notifications_api_sdk service API operations
"""

import pytest
import unittest
import datetime
# import json
# import os

from ibm_cloud_security_advisor.notifications_api_v1 import *
from ibm_cloud_security_advisor import NotificationsApiV1

from ibm_cloud_security_advisor.notifications_api_v1 import PublicKeyGet

from ibm_cloud_sdk_core import BaseService
from ibm_cloud_sdk_core import datetime_to_string, string_to_datetime

from unittest.mock import patch
from unittest import mock
m = mock.Mock()


class TestPublicKeyResponse(unittest.TestCase):
    app = {}
    @classmethod
    def setup_class(cls):
        print("\nrunning setup preparation...")
        TestPublicKeyResponse.app = PublicKeyGet(
             public_key="abc"
        )
        
        # read env vars
        #envvars = read_credentials()

    """_from_dict test cases """
    def test_from_dict_bad_key_neg(self):
        self.assertRaises(
            ValueError, PublicKeyResponse._from_dict, {"bad_key": "abc"})

    """_from_dict test cases """
    def test_from_dict_public_key_neg(self):
        self.assertRaises(
            ValueError, PublicKeyResponse._from_dict, {"public_key": "abc"})

    def test_from_dict_success(self):
        res = PublicKeyResponse._from_dict({
            "publicKey": "abc"
        })
        print(res)

    """_to_dict test cases """
    def test_to_dict_success(self):
        TestPublicKeyResponse.app.to_dict()

    """__eq__ test cases """

    def test__eq__isinstance(self):
        TestPublicKeyResponse.app.__eq__(TestPublicKeyResponse.app)

    def test__eq__not_isinstance(self):
        TestPublicKeyResponse.app.__eq__({})

    """__ne__ test cases """

    def test__ne__isinstance(self):
        TestPublicKeyResponse.app.__ne__(TestPublicKeyResponse.app)
