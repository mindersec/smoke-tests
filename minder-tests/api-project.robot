*** Settings ***
Resource   resources/keywords.robot
Library    resources.projects.Projects

Suite Setup    Load Config

Test Setup    Default Setup
Test Teardown    Default Teardown

*** Keywords ***
Default Setup
    Set Project as Environment Variable with Test Name

Default Teardown
    Remove Project Environment Variable for Test

*** Test Cases ***
Test List Roles API
    [Documentation]    Test the list of available roles in a project
    [Tags]    ProjectsService

    ${roles}=    Given Client Lists Roles
    Then Role List Format Is Valid    ${roles}
    Then Role List contains    ${roles}    admin
    Then Role List contains    ${roles}    editor
    Then Role List contains    ${roles}    viewer
    Then Role List contains    ${roles}    policy_writer
    Then Role List contains    ${roles}    permissions_manager
