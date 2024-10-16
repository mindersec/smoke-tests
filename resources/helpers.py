import os
import yaml
from sh import minder

from robot.api import logger
from resources.constants import MINDER_CONFIG, MINDER_OFFLINE_TOKEN_PATH, MINDER_API_ENDPOINT


def _get_url_from_config(server_type):
    """Helper function to read config and return URL for a given server type."""
    minder_config_path = os.getenv(MINDER_CONFIG)
    if not minder_config_path:
        raise Exception(f'{MINDER_CONFIG} environment variable is not set')

    try:
        with open(minder_config_path, 'r') as file:
            config = yaml.safe_load(file)

        host = config[f'{server_type}_server']['host']
        port = config[f'{server_type}_server']['port']

        if server_type == 'http':
            return f"http://{host}:{port}"
        else:
            return f"{host}:{port}"
    except KeyError as e:
        raise Exception(f"Missing expected configuration key: {e}")


def get_rest_url_from_config():
    """Reads the MINDER_CONFIG environment variable, loads the YAML config, and returns the REST BASE_URL."""
    try:
        return _get_url_from_config('http')
    except FileNotFoundError:
        return f'https://{MINDER_API_ENDPOINT}'


def get_grpc_url_from_config():
    """Reads the MINDER_CONFIG environment variable, loads the YAML config, and returns the gRPC BASE_URL."""
    try:
        return _get_url_from_config('grpc')
    except FileNotFoundError:
        return MINDER_API_ENDPOINT


def log_into_minder():
    logger.info('Logging into minder')
    if MINDER_OFFLINE_TOKEN_PATH not in os.environ:
        raise Exception(f'{MINDER_OFFLINE_TOKEN_PATH} env variable is not set')
    tokenpath = os.environ[MINDER_OFFLINE_TOKEN_PATH]
    if not tokenpath:
        raise Exception("MINDER_OFFLINE_TOKEN_PATH env variable is empty")

    logger.info(minder.auth('offline-token', 'use', '--file', tokenpath))
    return True
