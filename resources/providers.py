from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib
from resources.projects import Projects


class Providers:
    def __init__(self):
        self.rest_api = MinderRestApiLib()
        self.projects = Projects()

    @keyword
    def get_github_app_provider_id(self):
        """
        Retrieves the providers list and returns the ID of the first github-app provider.

        Returns:
            str: The name of the first github-app provider.

        Raises:
            ValueError: If no github-app provider is found.
        """
        try:
            return self._get_github_app_provider_id()
        except Exception as e:
            logger.error(f"Failed to get github-app provider: {str(e)}")
            raise

    def _get_github_app_provider_id(self):
        """
        Retrieves the providers list and returns the ID of the first github-app provider.

        Returns:
            str: The name of the first github-app provider.

        Raises:
            ValueError: If no github-app provider is found.
        """
        # Get the top-level project
        top_level_project = self.projects.get_toplevel_project()

        # Prepare the request parameters
        params = {"context.project": top_level_project}

        # Make the GET request to /api/v1/providers
        response = self.rest_api.get_request("/providers", params=params)

        # Extract the providers list from the response
        providers = response.get("providers", [])

        # Find the first github-app provider
        for provider in providers:
            if provider.get("class") == "github-app":
                logger.info(f"Found github-app provider: {provider['name']}")
                return provider["name"]

        raise ValueError("No github-app provider found")
