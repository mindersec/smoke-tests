from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import json
import os
import sh
import uuid
try:
    from sh import minder
except Exception:
    raise Exception('Minder CLI is not available')

rf = BuiltIn()

# Constants
MINDER_OFFLINE_TOKEN_PATH = 'MINDER_OFFLINE_TOKEN_PATH'

WHOAMI_OUT_KEY = 'whoami'
PROVIDER_LIST_OUT_KEY = 'provider-list'
PROJECT_LIST_OUT_KEY = 'project-list'


# Note that the class name must match the file name
class minderlib(object):
    """minderlib is a Robot Framework library for interacting with Minder

    It provides a set of keywords that can be used to interact with Minder
    from within Robot Framework test cases. Note that the lifetime of this
    library is tied to the lifetime of each test case. That is, each test
    case will have its own instance of this class.

    The class uses the variable __cmd_output to store the output of certain
    commands that have been executed. This is done to avoid having to run
    the same command multiple times. The __cmd_output variable is a dictionary
    that maps command identifiers to their output. The identifiers are strings.
    This is safe because a single test case runs serially and the class is
    instantiated for each test case.
    """
    def __init__(self):
        # cmd_output is a list of string identifiers that
        # tracks certain command outputs that have been
        # executed
        self.__cmd_output = dict()

    #####################################################################
    # Keywords
    #####################################################################

    def i_am_logged_into_minder(self):
        """I am logged into Minder

        This keyword logs into Minder using the offline token. The offline
        token is stored in the MINDER_OFFLINE_TOKEN_PATH environment variable.
        """
        logger.info('Logging into minder')
        if not MINDER_OFFLINE_TOKEN_PATH in os.environ:
            raise Exception(f'%s env variable is not set' % MINDER_OFFLINE_TOKEN_PATH)
        tokenpath = os.environ[MINDER_OFFLINE_TOKEN_PATH]
        if not tokenpath:
            raise Exception(f'%s env variable is empty' % MINDER_OFFLINE_TOKEN_PATH)

        logger.info(minder.auth('offline-token', 'use', '--file', tokenpath))
        return True

    def i_get_the_user_profile(self):
        """I get the user profile

        This keyword gets the user profile using the `auth whoami` subcommand.
        It stores the output in the __cmd_output dictionary using the constant
        WHOAMI_OUT_KEY as the key.
        """
        logger.info('Getting user profile')
        self.__cmd_output[WHOAMI_OUT_KEY] = minder.auth('whoami')
        logger.info(self.__cmd_output[WHOAMI_OUT_KEY])
        return self.__cmd_output[WHOAMI_OUT_KEY]

    def the_minder_server_should_be(self, server):
        """The Minder server should be

        This keyword checks if the Minder server is the one specified. It does
        this by checking the output of the `auth whoami` subcommand. The server
        name is passed as an argument to the keyword.

        Note that this requires the WHOAMI_OUT_KEY to be present in the
        __cmd_output dictionary. If it is not, an exception is raised.
        """
        logger.info('Checking minder server')
        self.__assert_cmd_output(WHOAMI_OUT_KEY)

        if not server in self.__cmd_output[WHOAMI_OUT_KEY]:
            raise Exception('No auth info available')
        
        for line in self.__cmd_output[WHOAMI_OUT_KEY].splitlines():
            if server in line:
                return True

    def i_list_my_providers(self):
        """I list my providers

        This keyword lists the providers that the user has access to. The output
        of the `provider list` subcommand is stored in the __cmd_output dictionary
        using the constant PROVIDER_LIST_OUT_KEY as the key.
        """
        return self.__list_minder_resources('provider', PROVIDER_LIST_OUT_KEY)

    def i_list_my_projects(self):
        """I list my projects

        This keyword lists the projects that the user has access to. The output
        of the `project list` subcommand is stored in the __cmd_output dictionary
        using the constant PROJECT_LIST_OUT_KEY as the key."""
        return self.__list_minder_resources('project', PROJECT_LIST_OUT_KEY)

    def i_should_have_at_least_one_provider_of_class(self, provider_class):
        """I should have at least one provider of class

        This keyword checks if there is at least one provider of the specified
        class. The provider class is passed as an argument to the keyword. The
        output of the `provider list` subcommand is used to check this.

        Note that this requires the PROVIDER_LIST_OUT_KEY to be present in the
        __cmd_output dictionary. If it is not, an exception is raised."""
        logger.info('Checking provider class')
        self.__assert_cmd_output(PROVIDER_LIST_OUT_KEY)

        list_out = self.__cmd_output[PROVIDER_LIST_OUT_KEY]
        if not 'providers' in list_out:
            raise Exception('No providers found')

        for provider in list_out['providers']:
            if 'class' in provider and provider['class'] == provider_class:
                return True

        raise Exception(f'No provider of class {provider_class} found')

    def i_should_have_at_least_one_project(self):
        """I should have at least one project

        This keyword checks if there is at least one project. The output of the
        `project list` subcommand is used to check this.

        Note that this requires the PROJECT_LIST_OUT_KEY to be present in the
        __cmd_output dictionary. If it is not, an exception is raised."""
        logger.info('Checking project')
        self.__assert_cmd_output(PROJECT_LIST_OUT_KEY)

        list_out = self.__cmd_output[PROJECT_LIST_OUT_KEY]
        if not 'projects' in list_out:
            raise Exception('No projects found')

        if len(list_out['projects']) > 0:
            return True

        raise Exception('No projects found')

    #####################################################################
    # Private methods / helpers
    #####################################################################

    def __list_minder_resources(self, resource_type : str, output_key : str):
        """List Minder resources

        This method lists Minder resources of the specified type. The resource
        type is passed as an argument to the method. The output of the command
        is stored in the __cmd_output dictionary using the output_key as the key.
        """
        logger.info(f'Listing {resource_type}s')
        resource_list = minder(resource_type, 'list', '-o', 'json')
        logger.info(resource_list)
        self.__cmd_output[output_key] = self.__parse_json(f'{resource_type}-list', resource_list)
        return True

    def __assert_cmd_output(self, identifier: str):
        if not identifier in self.__cmd_output:
            raise Exception(f'No {identifier} output available')

    @staticmethod
    def __parse_json(identifier: str, output: str):
        try:
            return json.loads(output)
        except Exception as e:
            raise Exception(f'Failed to parse {identifier}: {e}')
