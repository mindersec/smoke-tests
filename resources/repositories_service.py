import os
from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib
from resources.errors import ConfigurationError, APIError


class RepositoriesService:
    def __init__(self):
        self.rest_api = MinderRestApiLib()
        self.results = None

    @keyword
    def client_lists_repositories(self):
        """Lists registered repositories from the Minder API.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ConfigurationError: If required configuration is missing.
            APIError: If the API request fails.

        """
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {"context.project": project}

        try:
            self.results = self.rest_api.get_request("/repositories", params=params)
        except Exception as e:
            raise APIError(f"API request failed: {str(e)}")

    @keyword
    def get_results(self):
        """Lists registered repositories"""
        return self.results

    @keyword
    def repository_list_format_is_valid(self):
        """Verifies the structure of the evaluation results.

        Args:
            results (dict): The JSON response from the API.

        Raises:
            ValueError: If the results do not have the expected structure.

        """
        if not isinstance(self.results, dict):
            raise ValueError("Results should be a dictionary")

        if "results" not in self.results:
            raise ValueError("Response does not contain 'results' key")

        if not isinstance(self.results["results"], list):
            raise ValueError("'results' is not a list")

        logger.info("Evaluation results structure verified successfully")

    @keyword
    def repository_list_is_empty(self):
        """Verifies that the evaluation results are empty.

        Raises:
            ValueError: If the results are not empty.

        """
        if self.results["results"]:
            raise ValueError("Results should be empty")

    @keyword
    def repository_list_length_equals(self, length):
        """Verifies that the evaluation results are of the given
        length.

        Raises:
            ValueError: If the results are not empty.

        """
        if not len(self.results["results"]) == int(length):
            raise ValueError(
                f"Results should be {length} items long, was {len(self.results['results'])}"
            )
