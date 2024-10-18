*** Settings ***
Documentation    Test suite for some simple Minder operations

Test Tags    smoke

Library         resources.helpers
Library         resources/minderlib.py

Suite Setup     Set Grpc Base URL From Config


*** Variables ***
${PROVIDER_CLASS}       github-app
${GRPC_BASE_URL}        None   # Placeholder for the value that will be set in Suite Setup


*** Test Cases ***
Valid login
    [Documentation]    Test that a user can log in and get their profile
    [Tags]    login

    Given I Am Logged Into Minder
    When I Get The User Profile
    Then The Minder Server Should Be    ${GRPC_BASE_URL}

Provider enrolled
    [Documentation]    Test that a user has at least one provider

    Given I Am Logged Into Minder
    When I List My Providers
    Then I Should Have At Least One Provider Of Class    ${PROVIDER_CLASS}

Project created
    [Documentation]    Test that a user has at least one project

    Given I Am Logged Into Minder
    When I List My Projects
    Then I Should Have At Least One Project


*** Keywords ***
Set Grpc Base URL From Config
    [Documentation]    Reads the GRPC_BASE_URL from the config file and sets it for all tests.
    ${GRPC_BASE_URL}=    Get Grpc URL From Config
    Set Suite Variable    ${GRPC_BASE_URL}
