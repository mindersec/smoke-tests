import os
from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib


class EvalHistoryError(Exception):
    """Base exception for EvalHistoryService errors."""


class ConfigurationError(EvalHistoryError):
    """Raised when there's a configuration-related error."""


class APIError(EvalHistoryError):
    """Raised when there's an error in the API request or response."""


class EvalHistoryService:
    def __init__(self):
        self.history = None

    @keyword
    def client_retrieves_eval_history(self):
        """
        Retrieves evaluation history from the Minder API.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ConfigurationError: If required configuration is missing.
            APIError: If the API request fails.
        """
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        provider = os.getenv("MINDER_PROVIDER")
        if not provider:
            raise ConfigurationError("MINDER_PROVIDER environment variable is not set")

        params = {
            "provider": provider,
            "context.project": project
        }

        try:
            rest_api = MinderRestApiLib()
            self.history = rest_api.get_request('/history', params=params)
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")

    @keyword
    def history_format_is_valid(self):
        """
        Verifies the structure of the evaluation history.

        Args:
            history (dict): The JSON response from the API.

        Raises:
            ValueError: If the history do not have the expected structure.
        """
        if not isinstance(self.history, dict):
            raise ValueError("history should be a dictionary")

        if "data" not in self.history:
            raise ValueError("Response does not contain 'data' key")

        if not isinstance(self.history["data"], list):
            raise ValueError("'data' is not a list")

        logger.info("Evaluation history structure verified successfully")

    @keyword
    def history_is_empty(self):
        """
        Verifies that the evaluation history is empty.

        Raises:
            ValueError: If the history is not empty.
        """
        if self.history["data"]:
            raise ValueError("history should be empty")
