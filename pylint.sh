#!/bin/bash

echo 'linting...'

pylint ibm_cloud_security_advisor test --exit-zero
