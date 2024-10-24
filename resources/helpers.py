import os
import random
import yaml
from sh import minder

from robot.api import logger
from resources.constants import (
    MINDER_CONFIG,
    MINDER_OFFLINE_TOKEN_PATH,
    MINDER_API_ENDPOINT,
)


def randint():
    return f"{random.randint(1000000, 9999999)}"  # nosec B311


def _get_url_from_config(server_type):
    """Helper function to read config and return URL for a given server type."""
    minder_config_path = os.getenv(MINDER_CONFIG)
    if not minder_config_path:
        raise Exception(f"{MINDER_CONFIG} environment variable is not set")

    with open(minder_config_path, "r") as file:
        config = yaml.safe_load(file)

    host = config[f"{server_type}_server"].get("host", None)
    if not host:
        raise Exception(
            f"Missing expected configuration key: {server_type}_server.host"
        )
    port = config[f"{server_type}_server"].get("port", None)

    if server_type == "http":
        protocol = "http://"
        if port == 443:
            protocol = "https://"
        if port is None:
            return f"{protocol}{host}"
        return f"{protocol}{host}:{port}"
    else:
        if port is None:
            return host
        return f"{host}:{port}"


def get_rest_url_from_config():
    """Reads the MINDER_CONFIG environment variable, loads the YAML config, and returns the REST BASE_URL."""
    try:
        return _get_url_from_config("http")
    except FileNotFoundError:
        return f"https://{MINDER_API_ENDPOINT}"


def get_grpc_url_from_config():
    """Reads the MINDER_CONFIG environment variable, loads the YAML config, and returns the gRPC BASE_URL."""
    try:
        return _get_url_from_config("grpc")
    except FileNotFoundError:
        return MINDER_API_ENDPOINT


def log_into_minder():
    logger.info("Logging into minder")
    if MINDER_OFFLINE_TOKEN_PATH not in os.environ:
        raise Exception(f"{MINDER_OFFLINE_TOKEN_PATH} env variable is not set")
    tokenpath = os.environ[MINDER_OFFLINE_TOKEN_PATH]
    if not tokenpath:
        raise Exception("MINDER_OFFLINE_TOKEN_PATH env variable is empty")

    logger.info(minder.auth("offline-token", "use", "--file", tokenpath))
    return True
