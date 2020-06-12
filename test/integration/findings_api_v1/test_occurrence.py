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


class TestOccurrence(unittest.TestCase):
    ibm_security_advisor_findings_api_sdk = {}
    create_occ_resp = {}
    account_id = ""
    note_id = ""
    note_data = {}
    occ_data = {}

    @classmethod
    def setup_class(cls):
        print("running setup preparation...")
        # read env vars
        envvars = read_credentials()
        api_key = envvars['API_KEY']
        TestOccurrence.account_id = envvars['ACCOUNT_ID']
        findingsApiEndpoint = envvars['FINDING_API_ENDPOINT']
        iam_endpoint = envvars['IAM_ENDPOINT']

        # read note
        with open(jsonDir + "note.json") as f:
            TestOccurrence.note_data = json.load(f)
        
        TestOccurrence.note_data['id'] = generate_unique_string('note_occ')

        authenticator = IAMAuthenticator(
            url=iam_endpoint,
            apikey=api_key)
        TestOccurrence.ibm_security_advisor_findings_api_sdk = FindingsApiV1(
            authenticator=authenticator)
        TestOccurrence.ibm_security_advisor_findings_api_sdk.set_service_url(
            findingsApiEndpoint+"/findings")

        print("setup:creating note...")
        create_note_resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestOccurrence.account_id,
            **TestOccurrence.note_data
        )

        # read occurrence
        with open(jsonDir + "occurrence.json") as f:
            TestOccurrence.occ_data = json.load(f)
        TestOccurrence.occ_data['id'] = generate_unique_string('occ')
        print("setup:creating occurrence...")
        TestOccurrence.create_occ_resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_occurrence(
            account_id=TestOccurrence.account_id,
            note_name=TestOccurrence.account_id + "/providers/" + TestOccurrence.occ_data['provider_id'] + "/notes/" +
            TestOccurrence.note_data['id'],
            **TestOccurrence.occ_data
        )

    @classmethod
    def teardown_class(cls):
        print("running teardown, cleaning up the env...")
        print("teardown:delete note")
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestOccurrence.account_id,
            **TestOccurrence.note_data,
            note_id=TestOccurrence.note_data['id']
        )
        if response.result != {}:
            print("note deletion is failed", response)

        print("teardown:delete occurrence")
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_occurrence(
            account_id=TestOccurrence.account_id,
            **TestOccurrence.occ_data,
            occurrence_id=TestOccurrence.occ_data['id'],
        )
        if response.result != {}:
            print("occurrence deletion is failed", response)

    def test_create_occurrence(self):
        print("test create occurrence")
        assert TestOccurrence.create_occ_resp.result['id'] == TestOccurrence.occ_data['id']

    def test_create_occurrence_with_context(self):
        print("test create_occurrence_with_context")
        print("creating occurrence...")
        # read occurrence
        with open(jsonDir + "occurrence_with_context.json") as f:
            data = json.load(f)

        data['id'] = generate_unique_string('occ_with_context')

        resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_occurrence(
            account_id=TestOccurrence.account_id,
            note_name=TestOccurrence.account_id + "/providers/" + data['provider_id'] + "/notes/" +
            TestOccurrence.note_data['id'],
            **data
        )
        assert resp.result['id'] == data['id']
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_occurrence(
            account_id=TestOccurrence.account_id,
            occurrence_id=data['id'],
            **data
        )

    def test_create_occurrence_with_kpi(self):
        print("test_create_occurrence_with_kpi")
        print("creating kpi note")
        with open(jsonDir + "note_with_kpi.json") as f:
            note_data = json.load(f)
        note_data['id'] = generate_unique_string('kpi_note_occ')

        resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestOccurrence.account_id,
            **note_data
        )
        print("creating occurrence...")
        # read occurrence
        with open(jsonDir + "occurrence_with_kpi.json") as f:
            occ_data = json.load(f)
        occ_data['id'] = generate_unique_string('kpi_occ')

        resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_occurrence(
            account_id=TestOccurrence.account_id,
            note_name=TestOccurrence.account_id + "/providers/" + occ_data['provider_id'] + "/notes/" +
                      note_data['id'],
            **occ_data
        )
        assert resp.result['id'] == occ_data['id']

        delResp = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestOccurrence.account_id,
            **note_data,
            note_id=note_data['id']
        )
        if delResp.result != {}:
            print("note deletion is failed", delResp)
        
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_occurrence(
            account_id=TestOccurrence.account_id,
            occurrence_id=occ_data['id'],
            **occ_data
        )
        if response.result != {}:
            print("occurrence deletion is failed", response)

    def test_list_occurrence(self):
        print("test list occurrence")
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.list_occurrences(
            account_id=TestOccurrence.account_id,
            **TestOccurrence.occ_data,
        )
        # print("list occurrence",response)
        assert response.result['occurrences'][0]['id'] == TestOccurrence.occ_data['id']

    def test_list_note__occurrence(self):
        print("test list note occurrence")
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.list_note_occurrences(
            account_id=TestOccurrence.account_id,
            **TestOccurrence.note_data,
            note_id=TestOccurrence.note_data['id']
        )
        # print("list note occurrence",response)
        assert response.result['occurrences'][0]['id'] == TestOccurrence.occ_data['id']

    def test_delete_occurrence(self):
        print("test delete occurrence")
        print("creating occurrence for delete operation...")
        # read occurrence
        with open(jsonDir + "occurrence_for_delete_operation.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('occ_del')

        resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_occurrence(
            account_id=TestOccurrence.account_id,
            note_name=TestOccurrence.account_id + "/providers/" + data['provider_id'] + "/notes/" +
            TestOccurrence.note_data['id'],
            **data
        )
        response = TestOccurrence.ibm_security_advisor_findings_api_sdk.delete_occurrence(
            account_id=TestOccurrence.account_id,
            occurrence_id=data['id'],
            **data
        )
        # print("delete occurrence",response)
        assert response.result == {}

    def test_neg_create_occurrence_with_context(self):
        print("test_neg_create_occurrence_with_context")
        print("creating occurrence...")
        # read occurrence
        with open(jsonDir + "occurrence_with_context_neg.json") as f:
            data = json.load(f)
        data['id'] = generate_unique_string('occ_neg')
        try:
            resp = TestOccurrence.ibm_security_advisor_findings_api_sdk.create_occurrence(
                account_id=TestOccurrence.account_id,
                note_name=TestOccurrence.account_id + "/providers/" + data['provider_id'] + "/notes/" +
                          TestOccurrence.note_data['id'],
                **data
            )
        except ApiException as err:
            assert err.code == 400
