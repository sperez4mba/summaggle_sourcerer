# -*- coding: utf-8 -*-
import os

DEBUG = False
LOG_FILE_PATH = '/var/log/summaggle.log'
WTF_CSRF_ENABLED = True


class ConfigError(Exception):
    pass


def truthy(val):
    strval = str(val)
    return strval.lower() == 'true'


def env(name, default=None):
    no_env_config = truthy(os.environ.get("NO_ENV_CONFIG"))
    from_env = os.environ.get(name)
    if from_env is not None:
        return from_env

    if DEBUG and (default is not None):
        print("{} not found in environment, using default.".format(name))
        return default
    elif no_env_config:
        print("Bypassing env config for {}, using default.".format(name))
        return default
    else:
        raise ConfigError("{} not found in environment".format(name))


SECRET_KEY = env('SECRET_KEY', '123')
CSE_API_KEY = env('CSE_API_KEY', '123')
CSE_CONTEXT = env('CSE_CX', '123')

LOG_FILE_SIZE = int(env('LOG_FILE_SIZE', '10'))

#_MONGODB_AUTH_SOURCE = env('_MONGODB_AUTH_SOURCE', 'admin')
MONGODB_HOST = env('MONGODB_HOST', '127.0.0.1')
MONGODB_USER = env('MONGODB_USER', 'mongouser')
MONGODB_PASSWORD = env('MONGODB_PASSWORD', 'password')
MONGODB_NAME = env('MONGODB_NAME', 'mongodb')
MONGODB_CONN_CHAIN = "mongodb://{}:{}@{}/{}".format(
    MONGODB_USER,
    MONGODB_PASSWORD,
    MONGODB_HOST,
    MONGODB_NAME
)


# REDIS
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")


CELERY_BROKER_URL = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)
CELERY_DEFAULT_QUEUE='celery.summaggle'
CELERY_DEFAULT_EXCHANGE='celery.summaggle'
CELERY_BEAT_MAX_INTERVAL_IN_SECS = env('CELERY_BEAT_MAX_INTERVAL', '300')


UNSCRAPED_LINKS_CHECK_INTERVAL_IN_SECS = int(env('UNSCRAPED_LINKS_CHECK_INTERVAL_IN_SECS', '28800'))
