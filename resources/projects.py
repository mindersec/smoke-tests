from robot.api import logger
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
import re
import hashlib
import os
from resources.minder_restapi_lib import MinderRestApiLib


class Projects:
    @keyword
    def create_minder_project_with_test_name(self):
        """Creates a project in Minder using the current test name, converted to a DNS-safe name."""
        # Get the test name from Robot Framework
        test_name = BuiltIn().get_variable_value('${TEST NAME}')
        # Convert test name to DNS-safe name
        dns_safe_name = self._convert_to_dns_safe_name(test_name)
        return self._create_project(dns_safe_name)

    @keyword
    def remove_minder_project_with_test_name(self):
        """Removes a project in Minder using the current test name, converted to a DNS-safe name."""
        project_id = os.getenv("MINDER_PROJECT")
        if not project_id:
            raise ValueError("MINDER_PROJECT environment variable is not set")

        self._delete_project(project_id)

    @keyword
    def get_toplevel_project(self):
        """
        Retrieves the top-level project UUID from the /v1/user endpoint.

        Returns:
            str: The project UUID of the self-enrolled project.

        Raises:
            Exception: If the API request fails or the expected project is not found.
        """
        try:
            rest_api = MinderRestApiLib()
            data = rest_api.get_request('/user')
            logger.debug(f"Received response: {data}")

            for project in data.get('projects', []):
                if project.get('description') == "A self-enrolled project.":
                    logger.info(f"Found self-enrolled project with UUID: {project['projectId']}")
                    return project['projectId']

            raise Exception("No self-enrolled project found in the response")
        except Exception as e:
            raise Exception(f"Failed to get top-level project: {str(e)}")

    def _create_project(self, name):
        """
        Creates a project in Minder using the provided name.

        Args:
            name (str): The name of the project to create.

        Returns:
            str: The UUID of the created project.
        """
        # Get the top-level project
        top_level_project = self.get_toplevel_project()

        # Prepare the request body
        request_body = {
            "context": {
                "project": top_level_project
            },
            "name": name
        }

        # Make the POST request using MinderRestApiLib
        rest_api = MinderRestApiLib()
        response = rest_api.post_request('/projects', json=request_body)

        project_id = response.get('project', {}).get('projectId')
        if not project_id:
            raise ValueError("Project ID not found in the response")

        return project_id

    def _delete_project(self, project_id):
        """
        Deletes a project in Minder using the provided project ID.

        Args:
            project_id (str): The UUID of the project to delete.
        """
        rest_api = MinderRestApiLib()
        params = {
            "context.project": project_id
        }
        response = rest_api.delete_request('/projects', params=params)
        return response

    def _convert_to_dns_safe_name(self, name):
        """Convert a string to a DNS-safe name, adding a suffix only if necessary."""
        # Convert to lowercase
        name = name.lower()
        # Replace spaces and invalid characters with dashes
        name = re.sub(r'[^a-z0-9-]', '-', name)
        # Remove leading and trailing dashes
        name = name.strip('-')
        # Ensure it doesn't start with a number (prepend 'p-' if it does)
        if name[0].isdigit():
            name = 'p-' + name

        # If the name is already 63 characters or less, return it as is
        if len(name) <= 63:
            return name

        # Otherwise, truncate and add suffix
        suffix = hashlib.sha1(name.encode()).hexdigest()[:9]  # nosec
        truncated_name = name[:53]
        return f"{truncated_name}-{suffix}"
