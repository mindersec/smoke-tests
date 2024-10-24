import os
from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib
from resources.errors import ConfigurationError, APIError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


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

        params = {"provider": provider, "context.project": project}

        try:
            rest_api = MinderRestApiLib()
            self.history = rest_api.get_request("/history", params=params)
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

    @keyword
    def history_is_not_empty(self):
        """
        Verifies that the evaluation history is not empty.

        Raises:
            ValueError: If the history is empty.
        """
        if not self.history or not self.history.get("data"):
            raise ValueError("history should not be empty")

    @keyword
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(retry_if_exception_type(APIError) | retry_if_exception_type(ValueError)),
        reraise=True,
    )
    def client_retrieves_non_empty_eval_history(self):
        """
        Retrieves non-empty evaluation history from the Minder API with retries.
        Retries up to 3 times with exponential backoff between 1 and 10 seconds.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ConfigurationError: If required configuration is missing.
            APIError: If the API request fails after maximum retries.
            ValueError: If the history is empty after retrieval attempt.
        """
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        provider = os.getenv("MINDER_PROVIDER")
        if not provider:
            raise ConfigurationError("MINDER_PROVIDER environment variable is not set")

        params = {"provider": provider, "context.project": project}

        try:
            rest_api = MinderRestApiLib()
            self.history = rest_api.get_request("/history", params=params)
            if not self.history or not self.history.get("data"):
                raise ValueError("Retrieved history is empty")
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")

    @keyword
    def get_first_evaluation_history_id(self):
        """
        Retrieves the ID of the first evaluation history record.

        Returns:
            str: The ID of the first evaluation history record.

        Raises:
            ValueError: If the history is empty or no ID is found.
        """
        if not self.history or not self.history.get("data"):
            raise ValueError("No evaluation history data available")

        # Assuming 'data' is a list of EvaluationHistory objects
        first_record = self.history["data"][0]
        history_id = first_record.get("id")

        if not history_id:
            raise ValueError("No ID found in the first evaluation history record")

        return history_id

    @keyword
    def client_retrieves_eval_history_by_id(self, history_id):
        """
        Retrieves evaluation history by ID from the Minder API.

        Args:
            history_id (str): The ID of the history to retrieve.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ConfigurationError: If required environment variables are not set.
            APIError: If the API request fails.
        """

        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        provider = os.getenv("MINDER_PROVIDER")
        if not provider:
            raise ConfigurationError("MINDER_PROVIDER environment variable is not set")

        params = {"provider": provider, "context.project": project}

        try:
            rest_api = MinderRestApiLib()
            response = rest_api.get_request(f"/history/{history_id}", params=params)
            return response
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")
