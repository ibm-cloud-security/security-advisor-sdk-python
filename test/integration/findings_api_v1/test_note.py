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
from ibm_cloud_sdk_core.api_exception import ApiException

cwd = os.getcwd()
jsonDir = cwd + "/test/integration/findings_api_v1/input/json/"


class TestNote(unittest.TestCase):
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
        TestNote.account_id = envvars['ACCOUNT_ID']
        findingsApiEndpoint = envvars['FINDING_API_ENDPOINT']
        iam_endpoint = envvars['IAM_ENDPOINT']
        
		
        # read note
        with open(jsonDir + "note.json") as f:
            TestNote.note_data = json.load(f)
        TestNote.note_data['id'] = generate_unique_string('note')

        authenticator = IAMAuthenticator(
            url=iam_endpoint,
            apikey=api_key)
        TestNote.ibm_security_advisor_findings_api_sdk = FindingsApiV1(
            authenticator=authenticator)
        TestNote.ibm_security_advisor_findings_api_sdk.set_service_url(
            findingsApiEndpoint+"/findings")

        print("setup:creating note...")
        create_note_resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestNote.account_id,
            **TestNote.note_data
        )
        print(create_note_resp)

    @classmethod
    def teardown_class(cls):
        print("running teardown, cleaning up the env...")
        print("teardown:delete note")
        response = TestNote.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestNote.account_id,
            **TestNote.note_data,
            note_id=TestNote.note_data['id']
        )
        if response.result != {}:
            print("note deletion is failed", response)

    def test_list_note(self):
        print("test_list_note")
        resp = TestNote.ibm_security_advisor_findings_api_sdk.list_notes(
            account_id=TestNote.account_id,
            **TestNote.note_data,
        )
        assert resp.result['notes'][0]['id'] == TestNote.note_data['id']

    def test_delete_note(self):
        print("test_delete_note")
        # read note
        with open(jsonDir + "note_with_kpi.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('note')
        resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestNote.account_id,
            **data
        )
        delResp = TestNote.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestNote.account_id,
            **data,
            note_id=data['id']
        )

        assert delResp.result == {}

    def test_create_note_with_kpi(self):
        print("test_create_note_with_kpi")
        # read note
        with open(jsonDir + "note_with_kpi.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('kpi_note')
        resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestNote.account_id,
            **data
        )
        delResp = TestNote.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestNote.account_id,
            **data,
            note_id=data['id']
        )
        if delResp.result != {}:
            print("note deletion is failed", delResp)

        assert resp.result['id'] == data['id']

    def test_create_note_with_section(self):
        print("test_create_note_with_section")
        # read note
        with open(jsonDir + "note_with_section.json") as f:
            data = json.load(f)

        data['id'] = generate_unique_string('section_note')
        resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestNote.account_id,
            **data
        )

        delResp = TestNote.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestNote.account_id,
            **data,
            note_id=data['id']
        )
        if delResp.result != {}:
            print("note deletion is failed", delResp)

        assert resp.result['id'] == data['id']

    def test_create_card(self):
        print("test_create_card")
        # read note
        with open(jsonDir + "card.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('card')
        resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestNote.account_id,
            **data
        )

        delResp = TestNote.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestNote.account_id,
            **data,
            note_id=data['id']
        )
        if delResp.result != {}:
            print("note deletion is failed", delResp)

        assert resp.result['id'] == data['id']

    def test_neg_create_note_with_kpi(self):
        print("test_neg_create_note_with_kpi")
        # read note
        with open(jsonDir + "note_with_kpi_neg.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('kpi_note_neg')
        try:
            resp = TestNote.ibm_security_advisor_findings_api_sdk.create_note(
                account_id=TestNote.account_id,
                **data
            )
        except ApiException as err:
            assert err.code == 400
