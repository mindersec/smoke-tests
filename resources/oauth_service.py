import os
import re

from robot.api import logger
from robot.api.deco import keyword

from resources.errors import ConfigurationError, APIError
from resources.minder_restapi_lib import MinderRestApiLib

GITHUB_APP_PATTERN = r"https://github\.com/apps/[\w-]+/installations/new"
GITHUB_AUTHORIZATION_URL = r"https://github\.com/login/oauth/authorize?[\w-]+"


class OAuthService:
    def __init__(self):
        self.response = None

    @keyword
    def client_gets_authorization_url(self, provider_class):
        """Gets the authorization URL for enrolling a new provider.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ConfigurationError: If required configuration is missing.
            APIError: If the API request fails.

        """
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {
            # "provider": provider,
            "context.project": project,
            "provider_class": provider_class
        }

        try:
            rest_api = MinderRestApiLib()
            self.response = rest_api.get_request('/auth/url', params=params)
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")

    @keyword
    def response_format_is_valid(self):
        """
        Verifies the structure of the API response.

        Args:
            response (dict): The JSON response from the API.

        Raises:
            ValueError: If the response does not have the expected structure.
        """
        if not isinstance(self.response, dict):
            raise ValueError("Response should be a dictionary")

        if "url" not in self.response:
            raise ValueError("Response does not contain 'url' key")

        if "state" not in self.response:
            raise ValueError("Response does not contain 'state' key")

    logger.info("Get ruletype by name response structure verified successfully")

    @keyword
    def url_is_not_empty(self):
        """
        Verifies that the response contains a non-empty authorization URL.

        Raises:
            ValueError: If the URL field is empty.
        """
        if self.response["url"] == "":
            raise ValueError("URL should not be empty")

    @keyword
    def state_is_not_empty(self):
        """
        Verifies that the response contains a non-empty state.

        Raises:
            ValueError: If the state field is empty.
        """
        if self.response["state"] == "":
            raise ValueError("State should not be empty")

    @keyword
    def url_is_github_app_installation_page(self):
        """
        Verifies that the authorization URL is the GitHub App installation page.

        Raises:
            ValueError: If the URL does not match the expected pattern.
        """
        if not re.match(GITHUB_APP_PATTERN, self.response["url"]):
            raise ValueError("URL should match GitHub App installation page pattern")

    @keyword
    def url_is_authorization_code(self):
        """
        Verifies that the authorization URL is the GitHub OAuth authorization URL.

        Raises:
            ValueError: If the URL does not match the expected pattern.
        """
        if not re.match(GITHUB_AUTHORIZATION_URL, self.response["url"]):
            raise ValueError("URL should match GitHub OAuth authorization URL pattern")
