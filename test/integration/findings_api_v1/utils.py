# coding: utf-8

# Copyright 2019 IBM All Rights Reserved.
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
# from ibm_cloud_sdk_core.authenticators import Authenticator

import json as json_import
import uuid
from os import getenv, environ, getcwd
from os.path import isfile, join, expanduser

def read_credentials(separator: str = '=') -> dict:
    """Return a config object based on credentials file.

    Keyword Args:
        separator: The character to split on to de-serialize a line into a key-value pair.

    Returns:
        A set of configuration key-value pairs.
    """

    # read env vars
    config = {}
    env_keys = ['API_KEY', 'ACCOUNT_ID',
                'FINDING_API_ENDPOINT', 'IAM_ENDPOINT']
    is_read_from_file = False
    for k in env_keys:
        v = getenv(k)
        if k == 'IAM_ENDPOINT' and v is None:
            v = 'https://iam.cloud.ibm.com/identity/token'
        if v is not None:
            config[k] = v
        else:
            is_read_from_file = True
            break
    if(is_read_from_file):
        print("reading env vars from file... ")
        default_credentials_file_name = 'test/integration/input/cred/ibm-credentials.env'
        # File path specified by an env variable
        credential_file_path = getenv('IBM_CREDENTIALS_FILE')

        # Current working directory
        if credential_file_path is None:
            file_path = join(
                getcwd(), default_credentials_file_name)
            if isfile(file_path):
                credential_file_path = file_path

        # Home directory
        if credential_file_path is None:
            file_path = join(expanduser('~'), default_credentials_file_name)
            if isfile(file_path):
                credential_file_path = file_path

        if credential_file_path is not None:
            with open(credential_file_path, 'r') as fobj:
                for line in fobj:
                    key_val = line.strip().split(separator)
                    if len(key_val) == 2:
                        key = key_val[0]
                        value = key_val[1]
                        _parse_key_and_update_config(config, key, value)
    return config

def _parse_key_and_update_config(config, key, value):
    config[key] = value

def generate_unique_string(typ):
    """
    Generates a unique name based using Universally unique identifie.

    Keyword Args:
        typ: The type of element that will use the string.
    
    Returns:
        A a unique name.
    """
    return f'{uuid.uuid4().hex}_{typ}'

