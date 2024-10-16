import json
import os

from robot.api.deco import keyword
from robot.api import logger

from resources.helpers import log_into_minder


class MinderRestApiLib:
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

            # Extract the access token
            bearer_token = credentials.get('access_token')
            if not bearer_token:
                raise Exception("No access_token found in credentials file")

            logger.info("Successfully extracted Bearer token")
            return bearer_token
        except FileNotFoundError:
            raise Exception(f"Credentials file not found: {credentials_path}")
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse credentials file: {credentials_path}")
