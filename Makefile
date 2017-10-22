SHELL := /bin/bash

ifeq ($(wildcard .env.local), .env.local)
	LOCAL_ENV=`cat .env .env.local | egrep -v '^\#' | xargs`
else
  	LOCAL_ENV=`cat .env | egrep -v '^\#' | xargs`
endif


start-web:
	export SOURCERER_SETTINGS=`pwd`/config/config-prod.py && source env/bin/activate && `pwd`/manage prun


shell:
	export SOURCERER_SETTINGS=`pwd`/config/config-prod.py && source env/bin/activate && `pwd`/manage shell


test:
	export SOURCERER_SETTINGS=`pwd`/config/config-test.py && source env/bin/activate && nose2 -s . tests -v
