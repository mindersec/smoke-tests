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
Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

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
    Remove Environment Variable    MINDER_PROJECT
