#!/bin/bash
source dev-env/bin/activate
emulambda -v mubashir.lambda_handler test-event.json # need to generate events to test
deactivate
