*** Settings ***

Library    resources.helpers
Library    resources/minderlib.py
Suite Setup    Set Grpc Base URL From Config

*** Keywords ***
Set Grpc Base URL From Config
    [Documentation]    Reads the GRPC_BASE_URL from the config file and sets it for all tests.
    ${GRPC_BASE_URL}=    Get Grpc URL From Config
    Set Suite Variable    ${GRPC_BASE_URL}

*** Variables ***

${provider_class}   github-app

*** Test Cases ***

Valid login
    [Tags]    login   smoke
    Given I am logged into minder
    When I get the user profile
    Then the minder server should be    ${GRPC_BASE_URL}


Provider enrolled
    [Tags]    smoke
    Given I am logged into minder
    When I list my providers
    Then I should have at least one provider of class    ${provider_class}


Project created
    [Tags]    smoke
    Given I am logged into minder
    When I list my projects
    Then I should have at least one project