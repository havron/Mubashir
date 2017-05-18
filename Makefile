.PHONY: dev github deploy install clean

MSG=updated on `date`
DELIVER=deploy.zip

dev:
	./dev.sh
	# use emulambda here, ideally
deploy: # should upload to S3 bucket to link to on AWS Lambda (update link to source code)
	./deploy.sh	$(DELIVER)

github: clean
	git add -A
	git commit -m "${MSG}"
	git push

install: # makes the pyenvs and fills them up with libs. run once.
	./install.sh 

clean:
	rm -rf $(DELIVER) mubashir.pyc
