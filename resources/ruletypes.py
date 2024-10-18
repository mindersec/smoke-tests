import os
from sh import gh, minder
from robot.api.deco import keyword
from robot.api import logger


class Ruletypes:
    def __init__(self):
        self.path = os.getenv("MINDER_RULETYPES_PATH")
        if not self.path:
            raise ValueError("MINDER_RULETYPES_PATH environment variable is not set")
        # if the path does not exist or is not a directory, raise an error
        if not os.path.exists(self.path):
            raise ValueError(f"Path {self.path} does not exist")

        if not os.path.isdir(self.path):
            raise ValueError(f"Path {self.path} is not a directory")

    @keyword
    def ruletypes_are_ready(self):
        """
        Ensure that we have content in the ruletypes directory.
        """
        # if the directory is empty, clone the ruletypes repository from GitHub
        if not os.listdir(self.path):
            logger.info("Ruletypes directory is empty, cloning from GitHub")
            self._clone_ruletypes_from_github()

    @keyword
    def ruletypes_are_created(self):
        """
        Ensure that we have the ruletypes repository.
        """
        common_ruletypes = os.path.join(self.path, "rule-types", "common")
        minder.ruletype.create(f=common_ruletypes)

    @keyword
    def all_ruletypes_are_deleted(self):
        """
        Remove the ruletypes from minder.
        """
        logger.info(minder.ruletype.delete("--all", "--yes"))

    @keyword
    def installed_ruletypes_are_listed(self):
        """
        List the ruletypes from minder.
        """
        logger.info(minder.ruletype.list())

    def _clone_ruletypes_from_github(self):
        """
        Clone the ruletypes repository from GitHub.
        """
        logger.info(gh.repo.clone("mindersec/minder-rules-and-profiles", self.path))
