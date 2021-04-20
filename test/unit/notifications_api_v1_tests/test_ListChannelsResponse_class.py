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

from ibm_cloud_security_advisor import NotificationsApiV1

from ibm_cloud_security_advisor.notifications_api_v1 import ChannelsList
from ibm_cloud_security_advisor.notifications_api_v1 import ChannelInfo
from ibm_cloud_security_advisor.notifications_api_v1 import ChannelSeverity
from ibm_cloud_security_advisor.notifications_api_v1 import NotificationChannelAlertSourceItem

from ibm_cloud_sdk_core import BaseService
from ibm_cloud_sdk_core import datetime_to_string, string_to_datetime

from unittest.mock import patch
from unittest import mock
m = mock.Mock()


class TestListChannelsResponse(unittest.TestCase):
    app = {}
    @classmethod
    def setup_class(cls):
        print("\nrunning setup preparation...")
        channelResponseDefinitionSeverity = ChannelSeverity(
            high=True, medium=True, low=True
        )
        channelResponseDefinitionAlertSourceItem = NotificationChannelAlertSourceItem(
            provider_name="abc", finding_types=['abc']
        )
        channelResponseDefinition = ChannelInfo(
            channel_id="abc", name="abc", description="abc",
            type="abc", severity=channelResponseDefinitionSeverity,
            endpoint="http://abc.com", enabled=True,
            alert_source=[channelResponseDefinitionAlertSourceItem],
            frequency="abc"
        )
        TestListChannelsResponse.app = ChannelsList(
            channels=[channelResponseDefinition]
        )
        
        # read env vars
        #envvars = read_credentials()

    """_from_dict test cases """
    def test_from_dict_bad_key_neg(self):
        self.assertRaises(
            ValueError, ListChannelsResponse._from_dict, {"bad_key": "abc"})

    def test_from_dict_success(self):
        res = ListChannelsResponse._from_dict({
            "channels": [{}]
        })
        print(res)

    """_to_dict test cases """
    def test_to_dict_success(self):
        TestListChannelsResponse.app.to_dict()

    """__eq__ test cases """

    def test__eq__isinstance(self):
        TestListChannelsResponse.app.__eq__(TestListChannelsResponse.app)

    def test__eq__not_isinstance(self):
        TestListChannelsResponse.app.__eq__({})

    """__ne__ test cases """

    def test__ne__isinstance(self):
        TestListChannelsResponse.app.__ne__(TestListChannelsResponse.app)
