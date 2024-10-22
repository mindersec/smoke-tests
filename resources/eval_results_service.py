import os
from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib
from resources.errors import ConfigurationError, APIError


class EvalResultsService:
    def __init__(self):
        self.results = None

    @keyword
    def client_retrieves_eval_results(self):
        """
        Retrieves evaluation results from the Minder API.

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
            self.results = rest_api.get_request('/results', params=params)
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")

    @keyword
    def results_format_is_valid(self):
        """
        Verifies the structure of the evaluation results.

        Args:
            results (dict): The JSON response from the API.

        Raises:
            ValueError: If the results do not have the expected structure.
        """
        if not isinstance(self.results, dict):
            raise ValueError("Results should be a dictionary")

        if "entities" not in self.results:
            raise ValueError("Response does not contain 'entities' key")

        if not isinstance(self.results["entities"], list):
            raise ValueError("'entities' is not a list")

        logger.info("Evaluation results structure verified successfully")

    @keyword
    def results_are_empty(self):
        """
        Verifies that the evaluation results are empty.

        Raises:
            ValueError: If the results are not empty.
        """
        if self.results["entities"]:
            raise ValueError("Results should be empty")
