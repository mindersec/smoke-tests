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
Set Rest Base URL And Provider Environment Variables
    Set Rest Base URL From Config
    Set Provider as Environment Variable With Test Name

Remove Provider Environment Variable
    Remove Provider Environment Variable For Test

Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

Set Provider As Environment Variable With Test Name
    [Documentation]    Set the MINDER_PROVIDER environment variable to the first github-app provider

    # We might want to make this more dynamic in the future, but for now this is good enough
    ${GITHUB_APP_PROVIDER}=    Get Github App Provider ID
    Set Environment Variable    MINDER_PROVIDER    ${GITHUB_APP_PROVIDER}

Remove Provider Environment Variable For Test
    [Documentation]    Remove the provider environment variable after the test.
    Remove Environment Variable    MINDER_PROVIDER

Create Ruletypes
    [Documentation]    Create the ruletypes for the current project.

    Given I Am Logged Into Minder
    Given Ruletypes Are Ready
    When Ruletypes Are Created
    Then Installed Ruletypes Are Listed

Delete Ruletypes
    [Documentation]    Delete the ruletypes for the current project.

    Given I Am Logged Into Minder
    Given Ruletypes Are Ready
    When All Ruletypes Are Deleted
    Then Installed Ruletypes Are Listed

Set Project as Environment Variable With Test Name
    [Documentation]  Set the environment variable for the current test and log the test name.
    ${test_name}=    Create Minder Project With Test Name
    Set Environment Variable    MINDER_PROJECT    ${test_name}

Remove Project Environment Variable For Test
    [Documentation]    Remove the environment variable after the test.
    Remove Minder Project With Test Name
    Remove Environment Variable    MINDER_PROJECT
