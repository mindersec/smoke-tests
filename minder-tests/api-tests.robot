*** Settings ***
Documentation       Test suite for the Minder REST API

Resource   resources/keywords.robot
Resource   resources/variables.robot

Library    BuiltIn
Library    OperatingSystem
Library    RequestsLibrary
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.eval_results_service.EvalResultsService
Library    resources.rule_type_service.RuleTypeService

Suite Setup       Set Rest Base URL From Config

Test Setup      Create Project And Ruletypes
Test Teardown   Delete Ruletypes And Project


*** Test Cases ***
Test the User API with an authorized user
    [Documentation]    Test that an authorized user can retrieve info about self

    # Step 1: Login and create the Authorization header
    ${headers}=    Create Authorization Header

    # Step 2: Call the API endpoint with the Authorization header
    GET    ${BASE_URL}${API_ENDPOINT}/user    headers=${headers}

    Status Should Be    200

Test the User API with an unauthorized user
    [Documentation]    Test that an unauthorized user cannot retrieve info about self

    # Step 1: Call the API endpoint without the Authorization header
    GET    ${BASE_URL}${API_ENDPOINT}/user    expected_status=401

    Status Should Be    401

Test Evaluation Results API
    [Documentation]    Test that we can retrieve and verify evaluation results
    [Tags]    EvalResultsService

    When Client Retrieves Eval Results
    Given Results Format Is Valid
    Then Results Are Empty

Test Evaluation History API
    [Documentation]    Test that we can retrieve and verify evaluation history
    [Tags]    EvalHistoryService

    When Client Retrieves Eval History
    Given History Format Is Valid
    Then History Is Empty

Test Ruletype by name API
    [Documentation]    Test that we can retrieve a ruletype by name
    [Tags]    RuleTypeService

    When Client Retrieves Ruletype By Name    license
    Given Response Format Is Valid
    Then ID Is Not Empty
    And Display Name Is Not Empty

*** Keywords ***
Create Project And Ruletypes
    [Documentation]    Create the project and ruletypes for the current test.
    Set Project As Environment Variable With Test Name
    Create Ruletypes

Delete Ruletypes And Project
    [Documentation]    Delete the ruletypes and project for the current test.
    Delete Ruletypes
    Remove Project Environment Variable For Test
