import os


DEBUG = False
LOG_FILE_PATH = '/var/log/summaggle.log'


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


CSE_API_KEY = env('CSE_API_KEY', '123')
CSE_CONTEXT = env('CSE_CX', '123')

LOG_FILE_SIZE = int(env('LOG_FILE_SIZE', '10'))

#_MONGODB_AUTH_SOURCE = env('_MONGODB_AUTH_SOURCE', 'admin')
_MONGODB_HOST = env('_MONGODB_HOST', '127.0.0.1')
_MONGODB_USER = env('_MONGODB_USER', 'mongouser')
_MONGODB_PASSWORD = env('_MONGODB_PASSWORD', 'password')
_MONGODB_NAME = env('_MONGODB_NAME', 'mongodb')
_MONGODB_CONN_CHAIN = "mongodb://{}:{}@{}/{}".format(
    _MONGODB_USER,
    _MONGODB_PASSWORD,
    _MONGODB_HOST,
    _MONGODB_NAME
)
