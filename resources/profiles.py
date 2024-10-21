import json
import os

from robot.api import logger
from robot.api.deco import keyword
from resources.minder_restapi_lib import MinderRestApiLib
from resources.projects import Projects


class Profiles:
    def __init__(self):
        self.rest_api = MinderRestApiLib()
        self.profiles = []

    @keyword
    def client_adds_a_profile(self, profile_name, alert=False, remediate=False):
        alert_flag = "on" if alert else "off"
        remediate_flag = "on" if remediate else "off"

        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        profile = {
            "version": "v1",
            "type": "profile",
            "name": profile_name,
            "displayName": "Test Profile",
            "context": {
                "project": project,
            },
            "alert": alert_flag,
            "remediate": alert_flag,
            "repository": [
                {
                    "type": "license",
                    "name": "license",
                    "displayName": "License is valid",
                    "def": {
                        "license_filename": "LICENSE",
                        "license_type": "MIT",
                    },
                },
            ],
        }

        try:
            resp = self.rest_api.post_request("/profile", data=json.dumps({"profile": profile}))
            self.profiles.append(resp["profile"]["id"])
        except Exception as e:
            logger.error(f"Failed to create profile: {str(e)}")
            raise

    @keyword
    def delete_profile(self, profile_id):
        """Delete a Minder profile by ID."""
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {
            "context.project": project,
        }

        try:
            logger.info(self.rest_api.delete_request(f"/profile/{profile_id}", params=params))
        except Exception as e:
            logger.error(f"Failed to create profile: {str(e)}")
            raise

    @keyword
    def cleanup_minder_profiles(self):
        """Deletes all created profiles."""
        for profile_id in self.profiles:
            self.delete_profile(profile_id)

    @keyword
    def client_lists_profiles(self):
        """Lists available profiles."""
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {
            "context.project": project,
        }

        return self.rest_api.get_request("/profiles", params=params)

    @keyword
    def profiles_are_empty(self, profiles):
        if len(profiles["profiles"]):
            raise ValueError("Results should be empty")

    @keyword
    def profiles_are_not_empty(self, profiles):
        if not len(profiles["profiles"]):
            raise ValueError("Results should not be empty")
