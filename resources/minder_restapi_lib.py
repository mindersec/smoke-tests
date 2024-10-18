import json
import os
import requests
from robot.api.deco import keyword
from robot.api import logger

from resources.helpers import log_into_minder, get_rest_url_from_config


class MinderRestApiLib:
    def __init__(self):
        self.base_url = get_rest_url_from_config()
        self.api_endpoint = "/api/v1"

    @keyword
    def create_authorization_header(self):
        """Create Authorization Header

        Logs into Minder, extracts the Bearer token, and returns the Authorization header.
        """
        log_into_minder()
        bearer_token = self._get_bearer_token()

        # Return the Authorization header
        return {"Authorization": f"Bearer {bearer_token}"}

    def _get_bearer_token(self):
        """Extracts the Bearer token from the credentials.json file."""
        credentials_path = os.path.expanduser("~/.config/minder/credentials.json")
        try:
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)

            bearer_token = credentials.get('access_token')
            if not bearer_token:
                raise Exception("No access_token found in credentials file")

            logger.info("Successfully extracted Bearer token")
            return bearer_token
        except FileNotFoundError:
            raise Exception(f"Credentials file not found: {credentials_path}")
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse credentials file: {credentials_path}")

    def _make_request(self, method, path, **kwargs):
        url = f"{self.base_url}{self.api_endpoint}{path}"
        headers = self.create_authorization_header()
        headers.update(kwargs.pop('headers', {}))

        logger.info(f"Sending {method} request to {url}")
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    @keyword
    def get_request(self, path, **kwargs):
        return self._make_request('GET', path, **kwargs)

    @keyword
    def post_request(self, path, **kwargs):
        return self._make_request('POST', path, **kwargs)

    @keyword
    def delete_request(self, path, **kwargs):
        return self._make_request('DELETE', path, **kwargs)
