#!/bin/bash
virtualenv ../dev-env
virtualenv ../deploy-env
source ../dev-env/bin/activate
pip install git+https://github.com/fugue/emulambda.git
deactivate
