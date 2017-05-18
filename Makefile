.PHONY: dev github deploy install

MSG=updated on `date`
DELIVER=deploy.zip

dev:
		source dev-env/bin/activate
		emulambda -v test_event.lambda_handler test-event.json # need to generate events to test
		deactivate
		# use emulambda here, ideally
deploy: # should upload to S3 bucket to link to on AWS Lambda (update link to source code)
		source deploy-env/bin/activate
		rm $(DELIVER)
		cd deploy/lib/python2.7/site-packages && \
		zip -r9 ../../../../$(DELIVER) * && cd ../../../.. && \
		zip -g $(DELIVER) *.py && \
		aws s3 cp $(DELIVER) s3://mubashir-skill/
		deactivate
	
github:
		git add -A
		git commit -m "${MSG}"
		git push

install: # makes the pyenvs and fills them up with libs. run once.
		virtualenv ./dev-env
		virtualenv ./deploy-env
		source dev-env/bin/activate
		pip install git+https://github.com/fugue/emulambda.git
		deactivate
		source deploy-env/bin/activate
		# pip install
		deactivate
