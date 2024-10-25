*** Settings ***
Resource   resources/keywords.robot
Resource   resources/variables.robot

Library    OperatingSystem
Library    BuiltIn
Library    RequestsLibrary

Library    resources.helpers
Library    resources.projects.Projects
Library    resources.providers.Providers
Library    resources.minder_restapi_lib.MinderRestApiLib
Library    resources.repositories_service.RepositoriesService
Library    resources.github.GitHub
Library    resources.minderlib

Suite Setup    Load Config

Test Setup      Default Setup
Test Teardown   Default Teardown

*** Keywords ***
Default Setup
    Set Project as Environment Variable with Test Name
    ${MINDER_TEST_ORG}=    Get Environment Variable    MINDER_TEST_ORG
    Set Suite Variable    $MINDER_TEST_ORG

Default Teardown
    Remove Project Environment Variable for Test

*** Test Cases ***
Test the List Repositories API
    [Documentation]    Test that we can list repositories

    When Client Lists Repositories
    Then Repository List Format Is Valid
    Then Repository List is empty

Test the List Repositories API with registered repo
    [Documentation]    Test that we can list repositories

    ${test_repo}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo}
    Given repo is registered    ${test_repo}

    When Client Lists Repositories
    ${results}=    Get Results
    Log    ${results}
    Then Repository List Format Is Valid
    Then Repository List length equals    1

    [Teardown]    Run Keywords    Delete repo    ${test_repo}
    ...           AND    Default Teardown

Test the List Repositories API with multiple registered repos
    [Documentation]    Test that we can list repositories

    ${test_repo1}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo2}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo3}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo4}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python
    ${test_repo5}=    Given random repo name    ${MINDER_TEST_ORG}    smoke-test-python

    Given a copy of repo    stacklok/demo-repo-python    ${test_repo1}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo2}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo3}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo4}
    Given a copy of repo    stacklok/demo-repo-python    ${test_repo5}

    Given repo is registered    ${test_repo1}
    Given repo is registered    ${test_repo2}
    Given repo is registered    ${test_repo3}
    Given repo is registered    ${test_repo4}
    Given repo is registered    ${test_repo5}

    When Client Lists Repositories
    ${results}=    Get Results
    Log    ${results}
    Then Repository List Format Is Valid
    Then Repository List length equals    5

    [Teardown]    Run Keywords    Cleanup Minder Repos
    ...           AND    Cleanup GitHub Repos
    ...           AND    Default Teardown
