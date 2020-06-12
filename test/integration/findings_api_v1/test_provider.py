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
Test the  ibm_cloud_security_advisor service API operations
"""

import pytest
import unittest
import json
import os

from ibm_cloud_security_advisor import FindingsApiV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from .utils import read_credentials
from .utils import generate_unique_string

cwd = os.getcwd()
jsonDir = cwd + "/test/integration/findings_api_v1/input/json/"


class TestProvider(unittest.TestCase):
    ibm_security_advisor_findings_api_sdk = {}
    account_id = ""
    note_id = ""
    note_data = {}

    @classmethod
    def setup_class(cls):
        print("running setup preparation...")
        # read env vars
        envvars = read_credentials()
        api_key = envvars['API_KEY']
        TestProvider.account_id = envvars['ACCOUNT_ID']
        findingsApiEndpoint = envvars['FINDING_API_ENDPOINT']
        iam_endpoint = envvars['IAM_ENDPOINT']

        # read note
        with open(jsonDir + "note.json") as f:
            TestProvider.note_data = json.load(f)
        TestProvider.note_data['id'] = generate_unique_string('note')

        authenticator = IAMAuthenticator(
            url=iam_endpoint,
            apikey=api_key)
        TestProvider.ibm_security_advisor_findings_api_sdk = FindingsApiV1(
            authenticator=authenticator)
        TestProvider.ibm_security_advisor_findings_api_sdk.set_service_url(
            findingsApiEndpoint+"/findings")

        print("setup:creating note...")
        create_note_resp = TestProvider.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestProvider.account_id,
            **TestProvider.note_data
        )
        #print(create_note_resp)

    @classmethod
    def teardown_class(cls):
        print("running teardown, cleaning up the env...")
        print("teardown:delete note")
        response = TestProvider.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestProvider.account_id,
            **TestProvider.note_data,
            note_id=TestProvider.note_data['id']
        )
        if response.result != {}:
            print("note deletion is failed", response)

    def test_list_providers(self):
        print("test_list_providers")
        resp = TestProvider.ibm_security_advisor_findings_api_sdk.list_providers(
            account_id=TestProvider.account_id,
        )
        found = False
        for p in resp.result['providers']:
            if p['id'] == TestProvider.note_data['provider_id']:
                found = True
        assert found == True

    
