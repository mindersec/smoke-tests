*** Settings ***
Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Library    resources.helpers
Library    resources.projects.Projects
Library    resources.providers.Providers
Library    resources.ruletypes.Ruletypes
Library    resources.profiles.Profiles
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.minderlib

Suite Setup    Set Rest Base URL From Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Provider as Environment Variable with Test Name
    Set Project as Environment Variable with Test Name
    Ruletypes are created

Default Teardown
    Remove Provider Environment Variable for Test
    Remove Project Environment Variable for Test

Set Rest Base URL From Config
    [Documentation]    Reads the BASE_URL from the config file and sets it for all tests.
    ${BASE_URL}=    Get Rest URL From Config
    Set Suite Variable    ${BASE_URL}

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
Test the List Profile API
    [Documentation]    Test that we can create a profile

    ${profiles}=    When Client lists Profiles
    Then Profiles are empty    ${profiles}

Test the Create Profile API
    [Documentation]    Test that we can create a profile

    Given Client adds a Profile    test-profile
    ${profiles}=    When Client Lists Profiles
    Then Profiles are not empty    ${profiles}

    [Teardown]    Run Keywords    Cleanup Minder Profiles
    ...           AND    Default Teardown
