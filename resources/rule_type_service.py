import os

from robot.api import logger
from robot.api.deco import keyword

from resources.minder_restapi_lib import MinderRestApiLib


class RuleTypeError(Exception):
    """Base exception for RuleTypeService errors."""


class ConfigurationError(RuleTypeError):
    """Raised when there's a configuration-related error."""


class APIError(RuleTypeError):
    """Raised when there's an error in the API request or response."""


class RuleTypeService:
    def __init__(self):
        self.response = None

    @keyword
    def client_retrieves_ruletype_by_name(self, rule_name):
        """
        Retrieves a ruletype by name from the Minder API.

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
            "context.project": project,
        }

        try:
            rest_api = MinderRestApiLib()
            request_path = f"/rule_type/name/{rule_name}"
            self.response = rest_api.get_request(request_path, params=params)
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

        if "ruleType" not in self.response:
            raise ValueError("Response does not contain 'ruleType' key")

        if not isinstance(self.response["ruleType"], dict):
            raise ValueError("'ruleType' is not a dictionary")

        logger.info("Get ruletype by name response structure verified successfully")

    @keyword
    def id_is_not_empty(self):
        """
        Verifies that the response contains a non-empty ruletype ID.

        Raises:
            ValueError: If the ruletype ID is empty.
        """
        if self.response["ruleType"]["id"] == "":
            raise ValueError("Ruletype ID should not be empty")

    @keyword
    def display_name_is_not_empty(self):
        """
        Verifies that the response contains a ruletype display name.

        Raises:
            ValueError: If the ruletype display name is empty.
        """
        if self.response["ruleType"]["displayName"] == "":
            raise ValueError("Ruletype display name should not be empty")
