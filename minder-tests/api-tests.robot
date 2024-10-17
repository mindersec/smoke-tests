*** Settings ***
Library    resources.helpers
Library    resources.projects.Projects
Library    resources.providers.Providers
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.eval_results_service.EvalResultsService
Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Suite Setup    Set Rest Base URL From Config

Test Setup    Set Provider and Project as Environment Variables with Test Name
Test Teardown    Remove Provider and Project Environment Variables for Test

*** Variables ***
${API_ENDPOINT}    /api/v1/

*** Keywords ***
Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

Set Provider and Project as Environment Variables with Test Name
    Set Provider as Environment Variable with Test Name
    Set Project as Environment Variable with Test Name

Remove Provider and Project Environment Variables for Test
    Remove Provider Environment Variable for Test
    Remove Project Environment Variable for Test

Set Provider as Environment Variable with Test Name
    [Documentation]    Set the MINDER_PROVIDER environment variable to the first github-app provider

    # We might want to make this more dynamic in the future, but for now this is good enough
    ${GITHUB_APP_PROVIDER}=    Get Github App Provider ID
    Set Environment Variable    MINDER_PROVIDER    ${GITHUB_APP_PROVIDER}

Remove Provider Environment Variable for Test
    [Documentation]    Remove the provider environment variable after the test.
    Remove Environment Variable    MINDER_PROVIDER

Set Project as Environment Variable with Test Name
    [Documentation]  Set the environment variable for the current test and log the test name.
    ${test_name}=    Create Minder Project With Test Name
    Set Environment Variable    MINDER_PROJECT    ${test_name}

Remove Project Environment Variable for Test
    [Documentation]    Remove the environment variable after the test.
    Remove Minder Project With Test Name
    Remove Environment Variable    MINDER_PROJECT

*** Test Cases ***
Test the User API with an authorized user
    [Documentation]    Test that an authorized user can retrieve info about self

    # Step 1: Login and create the Authorization header
    ${headers}=    Create Authorization Header

    # Step 2: Call the API endpoint with the Authorization header
    ${response}=  GET    ${BASE_URL}${API_ENDPOINT}/user    headers=${headers}

    Status Should Be    200

Test the User API with an unauthorized user
    [Documentation]    Test that an unauthorized user cannot retrieve info about self

    # Step 1: Call the API endpoint without the Authorization header
    ${response}=  GET    ${BASE_URL}${API_ENDPOINT}/user    expected_status=401

    Status Should Be    401

Test Evaluation Results API
    [Documentation]    Test that we can retrieve and verify evaluation results
    [Tags]    EvalResultsService

    When Client Retrieves Eval Results
    Given Results Format Is Valid
    Then Results Are Empty
