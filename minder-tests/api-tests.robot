*** Settings ***
Resource   resources/keywords.robot
Resource   resources/variables.robot

Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.eval_results_service.EvalResultsService
Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Suite Setup       Set Rest Base URL and Provider Environment Variables
Suite Teardown    Remove Provider Environment Variable

Test Setup     Set Project as Environment Variable with Test Name
Test Teardown  Remove Project Environment Variable for Test


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
