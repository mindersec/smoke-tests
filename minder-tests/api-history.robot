*** Settings ***
Resource   resources/keywords.robot
Resource   resources/variables.robot

Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Library    resources.helpers
Library    resources.projects.Projects
Library    resources.profiles.Profiles
Library    resources.ruletypes.Ruletypes
Library    resources.github.GitHub
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.repositories_service.RepositoriesService
Library    resources.eval_history_service.EvalHistoryService

Suite Setup    Set Rest Base URL From Config

Test Setup      Default Setup
Test Teardown   Default Teardown

*** Keywords ***
Default Setup
    Set Provider as Environment Variable with Test Name
    Set Project as Environment Variable with Test Name
    Ruletypes are ready
    Ruletypes are created
    ${MINDER_TEST_ORG}=    Get Environment Variable    MINDER_TEST_ORG
    Set Suite Variable    $MINDER_TEST_ORG

Default Teardown
    Remove Provider Environment Variable for Test
    Remove Project Environment Variable for Test

*** Test Cases ***
Test Evaluation History By ID API
    [Documentation]    Test that we can retrieve and verify evaluation history by ID

    Given Client Adds A Profile    test-profile

    ${test_repo}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo}
    Given repo is registered    ${test_repo}

    When Client Retrieves Non Empty Eval History
    Given History Format Is Valid
    Then History Is Not Empty

    ${history_id}=    Get First Evaluation History ID
    ${record}=    Client Retrieves Eval History By ID    ${history_id}

    [Teardown]    Run Keywords    Cleanup Minder Profiles
    ...           AND    Cleanup Minder Repos
    ...           AND    Cleanup GitHub Repos
    ...           AND    Default Teardown
