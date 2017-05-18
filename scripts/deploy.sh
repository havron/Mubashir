#!/bin/bash
source ../deploy-env/bin/activate
rm -f $1
cd ../deploy-env/lib/python2.7/site-packages && \
zip -r9 ../../../../$1 * && cd ../../../.. && \
zip -g $1 *.py && \
aws s3 cp $1 s3://mubashir/
deactivate
