*** Settings ***
Library    resources.helpers
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    RequestsLibrary
Suite Setup    Set Rest Base URL From Config

*** Variables ***
${API_ENDPOINT}    /api/v1/

*** Keywords ***
Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

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