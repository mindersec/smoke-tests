*** Settings ***
Resource   resources/keywords.robot
Resource   resources/variables.robot

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
    Ruletypes are ready
    Ruletypes are created

Default Teardown
    Remove Provider Environment Variable for Test
    Remove Project Environment Variable for Test

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
