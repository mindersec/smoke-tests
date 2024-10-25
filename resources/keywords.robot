*** Settings ***
Library    resources.minderlib
Library    resources.helpers
Library    resources.projects.Projects
Library    resources.providers.Providers
Library    resources.ruletypes.Ruletypes
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.eval_results_service.EvalResultsService
Library    resources.eval_history_service.EvalHistoryService
Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

*** Keywords ***
Load Config
    [Documentation]    Reads tests' config file and sets useful variables for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}
    ${root_project}=    Get Environment Variable    MINDER_PROJECT
    Set Suite Variable    ${root_project}
    ${GRPC_BASE_URL}=    Get Grpc URL From Config
    Set Suite Variable    ${GRPC_BASE_URL}

Create Ruletypes
    [Documentation]    Create the ruletypes for the current project.

    Given I Am Logged Into Minder
    Given Ruletypes Are Ready
    When Ruletypes Are Created

Delete Ruletypes
    [Documentation]    Delete the ruletypes for the current project.

    Given I Am Logged Into Minder
    Given Ruletypes Are Ready
    When All Ruletypes Are Deleted

Set Project as Environment Variable With Test Name
    [Documentation]  Set the environment variable for the current test and log the test name.
    ${test_name}=    Create Minder Project With Test Name
    Set Environment Variable    MINDER_PROJECT    ${test_name}

Remove Project Environment Variable For Test
    [Documentation]    Remove the environment variable after the test.
    Remove Minder Project With Test Name
    Set Environment Variable    MINDER_PROJECT    ${root_project}
