from robot.api.deco import keyword
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
import json
import os
import sh
try:
    from sh import minder
except Exception:
    raise Exception('Minder CLI is not available')

rf = BuiltIn()

class MinderLibrary(object):
    def __init__(self):
        # cmd_output is a list of string identifiers that
        # tracks certain command outputs that have been
        # executed
        self.__cmd_output = dict()

    def i_am_logged_into_minder(self):
        logger.info('Logging into minder')
        if not 'MINDER_OFFLINE_TOKEN_PATH' in os.environ:
            raise Exception('MINDER_OFFLINE_TOKEN_PATH env variable is not set')
        tokenpath = os.environ['MINDER_OFFLINE_TOKEN_PATH']
        if not tokenpath:
            raise Exception('MINDER_OFFLINE_TOKEN_PATH env variable is empty')

        logger.info(minder.auth('offline-token', 'use', '--file', tokenpath))
        return True

    def i_get_the_user_profile(self):
        logger.info('Getting user profile')
        self.__cmd_output['whoami'] = minder.auth('whoami')
        logger.info(self.__cmd_output['whoami'])
        return self.__cmd_output['whoami']

    def the_minder_server_should_be(self, server):
        logger.info('Checking minder server')
        if not 'whoami' in self.__cmd_output:
            raise Exception('No whoami output available')

        if not server in self.__cmd_output['whoami']:
            raise Exception('No auth info available')
        
        # parse the auth info and search for the server
        for line in self.__cmd_output['whoami'].splitlines():
            if server in line:
                return True

    def i_list_my_providers(self):
        return self.__list_minder_resources('provider')

    def i_list_my_projects(self):
        return self.__list_minder_resources('project')

    def __list_minder_resources(self, resource_type):
        logger.info(f'Listing {resource_type}s')
        resource_list = minder(resource_type, 'list', '-o', 'json')
        logger.info(resource_list)
        self.__cmd_output[f'{resource_type}-list'] = self.__parse_json(f'{resource_type}-list', resource_list)
        return True

    def i_should_have_at_least_one_provider_of_class(self, provider_class):
        logger.info('Checking provider class')
        if not 'provider-list' in self.__cmd_output:
            raise Exception('No provider list available')
        list_out = self.__cmd_output['provider-list']
        for provider in list_out['providers']:
            if provider['class'] == provider_class:
                return True
        raise Exception(f'No provider of class {provider_class} found')

    def i_should_have_at_least_one_project(self):
        logger.info('Checking project')
        if not 'project-list' in self.__cmd_output:
            raise Exception('No project list available')
        list_out = self.__cmd_output['project-list']
        if len(list_out['projects']) > 0:
            return True
        raise Exception('No projects found')

    @staticmethod
    def __parse_json(identifier: str, output: str):
        try:
            return json.loads(output)
        except Exception as e:
            raise Exception(f'Failed to parse {identifier}: {e}')