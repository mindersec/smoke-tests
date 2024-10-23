*** Settings ***
Resource   resources/keywords.robot
Library    resources.projects.Projects

Suite Setup    Set Rest Base URL From Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Project as Environment Variable with Test Name

Default Teardown
    Remove Project Environment Variable for Test

*** Test Cases ***
Test List Roles API
    [Documentation]    Test that the authorization URL matches the GitHub App installation page
    [Tags]    OAuthService

    ${roles}=    Given Client Lists Roles
    Then Role List Format Is Valid    ${roles}
    Then Role List contains    ${roles}    admin
    Then Role List contains    ${roles}    editor
    Then Role List contains    ${roles}    viewer
    Then Role List contains    ${roles}    policy_writer
    Then Role List contains    ${roles}    permissions_manager
