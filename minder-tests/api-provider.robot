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
Library    resources.oauth_service.OAuthService

Suite Setup    Set Rest Base URL From Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Project as Environment Variable with Test Name

Default Teardown
    Remove Project Environment Variable for Test

*** Test Cases ***
Test Authorization URL API for GitHub App
    [Documentation]    Test that the authorization URL matches the GitHub App installation page
    [Tags]    OAuthService

    When Client Gets Authorization Url    github-app
    Given Response Format Is Valid
    Then URL Is Not Empty
    And URL Is GitHub App Installation Page
    And State Is Not Empty

Test Authorization URL API for GitHub OAuth
    [Documentation]    Test that the authorization URL matches the GitHub OAuth authorization URL
    [Tags]    OAuthService

    When Client Gets Authorization Url    github
    Given Response Format Is Valid
    Then URL Is Not Empty
    And URL Is Authorization Code
    And State Is Not Empty