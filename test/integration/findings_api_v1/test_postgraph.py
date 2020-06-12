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


class TestPostGraph(unittest.TestCase):
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
        TestPostGraph.account_id = envvars['ACCOUNT_ID']
        findingsApiEndpoint = envvars['FINDING_API_ENDPOINT']
        iam_endpoint = envvars['IAM_ENDPOINT']

        # read note
        with open(jsonDir + "note.json") as f:
            TestPostGraph.note_data = json.load(f)
        TestPostGraph.note_data['id'] = generate_unique_string('note_graph')

        authenticator = IAMAuthenticator(
            url=iam_endpoint,
            apikey=api_key)
        TestPostGraph.ibm_security_advisor_findings_api_sdk = FindingsApiV1(
            authenticator=authenticator)
        TestPostGraph.ibm_security_advisor_findings_api_sdk.set_service_url(
            findingsApiEndpoint+"/findings")

        print("setup:creating note...")
        create_note_resp = TestPostGraph.ibm_security_advisor_findings_api_sdk.create_note(
            account_id=TestPostGraph.account_id,
            **TestPostGraph.note_data
        )

        # read occurrence
        with open(jsonDir + "occurrence.json") as f:
            TestPostGraph.occ_data = json.load(f)
        TestPostGraph.occ_data['id'] = generate_unique_string('occ_graph')
        

        print("setup:creating occurrence...")
        TestPostGraph.create_occ_resp = TestPostGraph.ibm_security_advisor_findings_api_sdk.create_occurrence(
            account_id=TestPostGraph.account_id,
            note_name=TestPostGraph.account_id + "/providers/" + TestPostGraph.occ_data['provider_id'] + "/notes/" +
            TestPostGraph.note_data['id'],
            **TestPostGraph.occ_data
        )

    @classmethod
    def teardown_class(cls):
        print("running teardown, cleaning up the env...")
        print("teardown:delete note")
        response = TestPostGraph.ibm_security_advisor_findings_api_sdk.delete_note(
            account_id=TestPostGraph.account_id,
            **TestPostGraph.note_data,
            note_id=TestPostGraph.note_data['id']
        )
        if response.result != {}:
            print("note deletion is failed", response)

        print("teardown:delete occurrence")
        response = TestPostGraph.ibm_security_advisor_findings_api_sdk.delete_occurrence(
            account_id=TestPostGraph.account_id,
            **TestPostGraph.occ_data,
            occurrence_id=TestPostGraph.occ_data['id'],
        )
        if response.result != {}:
            print("occurrence deletion is failed", response)

    def test_post_graph(self):
        print("test_post_graph")
        query="query {occurrence(providerId:\""+TestPostGraph.occ_data['provider_id']+"\",id:\""+TestPostGraph.occ_data['id']+"\") {name id}}"
        resp = TestPostGraph.ibm_security_advisor_findings_api_sdk.post_graph(
            account_id=TestPostGraph.account_id,
            body=query,
            content_type="application/graphql"
        )
        #print(resp)
        assert resp.result['data']['occurrence']['id'] == TestPostGraph.occ_data['id']

    def test_neg_post_graph(self):
        print("test_neg_post_graph")
        query="query {occurrence(providerId:\""+TestPostGraph.occ_data['provider_id']+"\") {name id}}"
        try:
            resp = TestPostGraph.ibm_security_advisor_findings_api_sdk.post_graph(
                account_id=TestPostGraph.account_id,
                body=query,
                content_type="application/graphql"
            )
        except ApiException as err:
            assert err.code == 400

