import json
import os

from robot.api import logger
from robot.api.deco import keyword

from resources.errors import ConfigurationError
from resources.minder_restapi_lib import MinderRestApiLib


class DataSources:
    def __init__(self):
        self.rest_api = MinderRestApiLib()
        self.datasources = dict()

    @keyword
    def client_lists_data_sources(self):
        """Lists available data sources."""
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {
            "context.project_id": project,
        }

        return self.rest_api.get_request("/data_sources", params=params)

    @keyword
    def client_adds_a_data_source(self, data_source_name):
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        data_source = {
            "version": "v1",
            "type": "data-source",
            "name": data_source_name,
            "context": {
                "project_id": project,
            },
            "rest": {
                "def": {
                    "license": {
                        "endpoint": "https://raw.githubusercontent.com/spdx/license-list-data/refs/heads/main/json/licenses.json",
                        "parse": "json",
                        "input_schema": {},
                    }
                }
            }
        }

        try:
            resp = self.rest_api.post_request(
                "/data_source", data=json.dumps({"dataSource": data_source})
            )
            self.datasources[resp["dataSource"]["name"]] = resp["dataSource"]
        except Exception as e:
            logger.error(f"Failed to create data source: {str(e)}")
            raise

    @keyword
    def client_updates_a_data_source(self, data_source_name):
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        data_source = self.datasources[data_source_name]
        if not data_source:
            raise ConfigurationError(f"No data sources created for {data_source_name}")

        data_source["rest"]["def"]["license"]["endpoint"] = "https://github.com"
        logger.info(f"updating datasource {data_source}")

        try:
            resp = self.rest_api.put_request(
                "/data_source",
                data=json.dumps({"dataSource": data_source}),
            )
            self.datasources[resp["dataSource"]["name"]] = resp["dataSource"]
        except Exception as e:
            logger.error(f"Failed to update data source: {str(e)}")
            raise

    @keyword
    def delete_data_source(self, data_source_id):
        """Delete a Minder data source by ID."""
        project = os.getenv("MINDER_PROJECT")
        if not project:
            raise ConfigurationError("MINDER_PROJECT environment variable is not set")

        params = {
            "context.project_id": project,
        }

        try:
            logger.info(
                self.rest_api.delete_request(f"/data_source/{data_source_id}", params=params)
            )
        except Exception as e:
            logger.error(f"Failed to delete data source: {str(e)}")
            raise

    @keyword
    def cleanup_minder_data_sources(self):
        """Deletes all created data sources."""
        for datasource in self.datasources.values():
            logger.info(f"cleaning up datasource {datasource}")
            self.delete_data_source(datasource["id"])

    @keyword
    def data_sources_are_empty(self, data_sources):
        if len(data_sources["dataSources"]):
            raise ValueError("Results should be empty")

    @keyword
    def data_sources_are_not_empty(self, data_sources):
        if not len(data_sources["dataSources"]):
            raise ValueError("Results should not be empty")
