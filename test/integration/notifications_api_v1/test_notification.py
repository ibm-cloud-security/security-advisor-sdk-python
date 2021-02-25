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
import json
import os

from ibm_cloud_security_advisor import NotificationsApiV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .utils import read_credentials
from ibm_cloud_sdk_core.api_exception import ApiException
from .utils import generate_unique_name

cwd = os.getcwd()
jsonDir = cwd + "/test/integration/notifications_api_v1/input/json/"


class TestNotification(unittest.TestCase):
    ibm_security_advisor_notifications_api_sdk = {}
    account_id = ""
    notification_data = {},
    create_notification_channel_resp = {}
    @classmethod
    def setup_class(cls):
        print("running setup preparation...")
        # read env vars
        envvars = read_credentials()
        api_key = envvars['API_KEY']
        TestNotification.account_id = envvars['ACCOUNT_ID']
        notificationApiEndpoint = envvars['NOTIFICATION_API_ENDPOINT']
        iam_endpoint = envvars['IAM_ENDPOINT']

        authenticator = IAMAuthenticator(
            url=iam_endpoint,
            apikey=api_key)
        TestNotification.ibm_security_advisor_notifications_api_sdk = NotificationsApiV1(
            authenticator=authenticator)
        TestNotification.ibm_security_advisor_notifications_api_sdk.set_service_url(
            notificationApiEndpoint+"/notifications")

        # read notification json
        with open(jsonDir + "notification.json") as f:
            TestNotification.notification_data = json.load(f)
        
        TestNotification.notification_data[0]['name'] = generate_unique_name()
        TestNotification.create_notification_channel_resp = TestNotification.ibm_security_advisor_notifications_api_sdk.create_notification_channel(
            account_id=TestNotification.account_id,
            **TestNotification.notification_data[0]
        )
        
    @classmethod
    def teardown_class(cls):
        print("running teardown, cleaning up the env...")
        response = TestNotification.ibm_security_advisor_notifications_api_sdk.delete_notification_channel(
            account_id=TestNotification.account_id,
            channel_id=TestNotification.create_notification_channel_resp.result['channel_id'],
        )
        if response.result['message'] != "Success":
            print("notification channel deletion is failed", response)

    def test_list_all_channels(self):
        print("test_list_all_channels...")
        resp = TestNotification.ibm_security_advisor_notifications_api_sdk.list_all_channels(
            account_id=TestNotification.account_id
        )
        assert resp.status_code == 200

    def test_create_notification_channel(self):
        print("test_create_notification_channel...")
        assert TestNotification.create_notification_channel_resp.result['status_code'] == 200

    def test_delete_notification_channels(self):
        print("test_delete_notification_channels...")
        TestNotification.notification_data[1]['name'] = generate_unique_name()
        resp1 = TestNotification.ibm_security_advisor_notifications_api_sdk.create_notification_channel(
            account_id=TestNotification.account_id,
            **TestNotification.notification_data[1]
        )
        assert resp1.result['status_code'] == 200

        TestNotification.notification_data[3]['name'] = generate_unique_name()
        resp2 = TestNotification.ibm_security_advisor_notifications_api_sdk.create_notification_channel(
            account_id=TestNotification.account_id,
            **TestNotification.notification_data[3]
        )

        assert resp2.result['status_code'] == 200
        del_resp = TestNotification.ibm_security_advisor_notifications_api_sdk.delete_notification_channels(
            account_id=TestNotification.account_id,
            body=[
                    resp1.result['channel_id'],
                    resp2.result['channel_id']
                ]
        )
        assert del_resp.result['message'] == "Success"

    def test_delete_notification_channel(self):
        print("test_delete_notification_channel...")

        TestNotification.notification_data[1]['name'] = generate_unique_name()
        resp = TestNotification.ibm_security_advisor_notifications_api_sdk.create_notification_channel(
            account_id=TestNotification.account_id,
            **TestNotification.notification_data[1]
        )
        assert resp.result['status_code'] == 200
        del_resp = TestNotification.ibm_security_advisor_notifications_api_sdk.delete_notification_channel(
            account_id=TestNotification.account_id,
            channel_id=resp.result['channel_id'],
        )
        assert del_resp.result['message'] == "Success"

    def test_get_notification_channel(self):
        print("test_delete_notification_channel...")
        resp = TestNotification.ibm_security_advisor_notifications_api_sdk.get_notification_channel(
            account_id=TestNotification.account_id,
            channel_id=TestNotification.create_notification_channel_resp.result['channel_id']
        )
        assert resp.result['channel']['name'] == TestNotification.notification_data[0]['name']

    def test_update_notification_channel(self):
        print("test_update_notification_channel...")
        TestNotification.notification_data[2]['name'] = generate_unique_name()
        resp = TestNotification.ibm_security_advisor_notifications_api_sdk.update_notification_channel(
            account_id=TestNotification.account_id,
            channel_id=TestNotification.create_notification_channel_resp.result['channel_id'],
            **TestNotification.notification_data[2]
        )
        assert resp.result['status_code'] == 200
        
    def test_get_public_key(self):
        print("test_get_public_key...")
        resp = TestNotification.ibm_security_advisor_notifications_api_sdk.get_public_key(
                account_id=TestNotification.account_id,
            )
        assert 'public_key' in resp.result
