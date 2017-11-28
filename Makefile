SHELL := /bin/bash

ifeq ($(wildcard .env.local), .env.local)
	LOCAL_ENV = env `cat .env .env.local | egrep -v '^\#' | xargs`
else
	LOCAL_ENV = env `cat .env | egrep -v '^\#' | xargs`
endif


start-dev-web:
	export SOURCERER_SETTINGS=`pwd`/config/config-local.py && source virtualenv/bin/activate && `pwd`/manage prun


start-tasks:
	export SOURCERER_SETTINGS=`pwd`/config/config-prod.py && source virtualenv/bin/activate && `pwd`/manage celery_worker_up


shell:
	export SOURCERER_SETTINGS=`pwd`/config/config-prod.py && source virtualenv/bin/activate && `pwd`/manage shell


test:
	export SOURCERER_SETTINGS=`pwd`/config/config-test.py && source virtualenv/bin/activate && nose2 -s . tests -v


ci-test:
	export SOURCERER_SETTINGS=`pwd`/config/config-test.py && nose2 -s . tests -v


start-web:
	$(LOCAL_ENV) SOURCERER_SETTINGS=`pwd`/config/config-local.py && source virtualenv/bin/activate && gunicorn -w 4 -b 0.0.0.0:4000 sourcerer:app
